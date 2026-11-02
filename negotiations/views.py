from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction, models
from django.db.models import Sum
from django.http import JsonResponse
from django.utils import timezone
from accounts.decorators import buyer_required, farmer_required
from marketplace.models import CropListing
from contracts.models import Contract
from deliveries.models import Delivery
from payments.models import Payment
from .models import Offer, NegotiationMessage
from .forms import OfferForm, CounterOfferForm
from notifications.services import send_user_notification
from audit.models import AuditLog

@buyer_required
def buyer_dashboard(request):
    """Buyer Command Center: procurement volume, active deals, contracts, and delivery schedules."""
    user = request.user
    my_offers = Offer.objects.filter(buyer=user)
    contracts = Contract.objects.filter(buyer=user)

    available_crops_count = CropListing.objects.filter(status=CropListing.Status.ACTIVE).count()
    active_contracts_count = contracts.filter(status=Contract.Status.ACTIVE).count()
    completed_contracts_count = contracts.filter(status=Contract.Status.COMPLETED).count()

    pending_offers_count = my_offers.filter(status__in=[Offer.Status.PENDING, Offer.Status.COUNTERED]).count()

    upcoming_arrivals = Delivery.objects.filter(
        contract__buyer=user,
        status__in=[Delivery.Status.SCHEDULED, Delivery.Status.READY_FOR_DISPATCH, Delivery.Status.IN_TRANSIT]
    ).count()

    total_spend = Payment.objects.filter(
        payer=user,
        status=Payment.Status.SUCCESS
    ).aggregate(total=models.Sum("amount"))["total"] or 0

    pending_pay_obligations = Payment.objects.filter(
        payer=user,
        status=Payment.Status.PENDING
    ).aggregate(total=models.Sum("amount"))["total"] or 0

    recent_offers = my_offers.select_related("crop_listing", "crop_listing__farmer")[:5]
    recent_contracts = contracts.select_related("farmer")[:5]

    context = {
        "available_crops_count": available_crops_count,
        "active_contracts_count": active_contracts_count,
        "completed_contracts_count": completed_contracts_count,
        "pending_offers_count": pending_offers_count,
        "upcoming_arrivals": upcoming_arrivals,
        "total_spend": total_spend,
        "pending_pay_obligations": pending_pay_obligations,
        "recent_offers": recent_offers,
        "recent_contracts": recent_contracts,
    }
    return render(request, "buyer/dashboard.html", context)


@buyer_required
def buyer_offers_list(request):
    """List of all procurement offers submitted by the logged-in buyer."""
    offers = Offer.objects.filter(buyer=request.user).select_related("crop_listing", "crop_listing__farmer")
    return render(request, "buyer/offers/list.html", {"offers": offers})


@farmer_required
def farmer_offers_list(request):
    """List of all purchase offers received by the logged-in farmer."""
    offers = Offer.objects.filter(crop_listing__farmer=request.user).select_related("buyer", "crop_listing")
    return render(request, "farmer/offers/list.html", {"offers": offers})


@buyer_required
def offer_create(request, crop_id):
    """Buyer submits a formal offer on a crop listing."""
    crop = get_object_or_404(CropListing, pk=crop_id, status=CropListing.Status.ACTIVE)

    if crop.farmer == request.user:
        messages.error(request, "You cannot submit an offer on your own crop listing.")
        return redirect("crop_detail", pk=crop.id)

    if request.method == "POST":
        form = OfferForm(request.POST)
        if form.is_valid():
            qty = form.cleaned_data["quantity_kg"]
            price = form.cleaned_data["proposed_price_per_kg"]

            if qty > crop.available_quantity_kg:
                form.add_error("quantity_kg", f"Requested quantity exceeds available stock ({crop.available_quantity_kg} kg).")
            elif price <= 0:
                form.add_error("proposed_price_per_kg", "Price per kg must be greater than zero.")
            else:
                with transaction.atomic():
                    offer = form.save(commit=False)
                    offer.crop_listing = crop
                    offer.buyer = request.user
                    offer.status = Offer.Status.PENDING
                    offer.current_turn = Offer.Turn.FARMER
                    offer.save()

                    # Save initial message if provided
                    if offer.message:
                        NegotiationMessage.objects.create(
                            offer=offer,
                            sender=request.user,
                            recipient=crop.farmer,
                            message=offer.message,
                            counter_price_per_kg=offer.proposed_price_per_kg,
                            counter_quantity_kg=offer.quantity_kg,
                            counter_delivery_date=offer.delivery_date
                        )

                    AuditLog.log(
                        "OFFER_SUBMITTED",
                        "Offer",
                        offer.id,
                        f"Buyer {request.user.username} offered ₹{offer.proposed_price_per_kg}/kg for {offer.quantity_kg}kg of {crop.crop_name}",
                        user=request.user
                    )

                    send_user_notification(
                        crop.farmer,
                        f"New Offer Received for {crop.crop_name}",
                        f"Buyer {request.user.get_full_name() or request.user.username} submitted an offer of ₹{offer.proposed_price_per_kg}/kg for {offer.quantity_kg} kg.",
                        notification_type="OFFER",
                        link_url=f"/negotiations/offers/{offer.id}/"
                    )

                    messages.success(request, f"Your offer of ₹{offer.proposed_price_per_kg}/kg for {offer.quantity_kg} kg has been sent to the farmer.")
                    return redirect("offer_detail", offer_id=offer.id)
    else:
        initial_data = {
            "proposed_price_per_kg": crop.expected_price_per_kg,
            "quantity_kg": min(crop.available_quantity_kg, 1000),
            "delivery_date": crop.expected_harvest_date,
        }
        form = OfferForm(initial=initial_data)

    return render(request, "negotiations/offer_create.html", {"form": form, "crop": crop})


@login_required
def offer_detail(request, offer_id):
    """Detailed negotiation hub showing commercial terms, live discussion history, counter-offer form, and actions."""
    offer = get_object_or_404(
        Offer.objects.select_related("crop_listing", "crop_listing__farmer", "buyer"),
        pk=offer_id
    )

    # Permission check: user must be the buyer or the farmer
    if request.user != offer.buyer and request.user != offer.crop_listing.farmer and not request.user.is_platform_admin():
        messages.error(request, "Unauthorized access to negotiation thread.")
        return redirect("dashboard")

    messages_list = offer.messages.all().select_related("sender")
    counter_form = CounterOfferForm()

    is_farmer = (request.user == offer.crop_listing.farmer)
    is_buyer = (request.user == offer.buyer)
    can_act = (offer.status in [Offer.Status.PENDING, Offer.Status.COUNTERED])

    context = {
        "offer": offer,
        "messages_list": messages_list,
        "counter_form": counter_form,
        "is_farmer": is_farmer,
        "is_buyer": is_buyer,
        "can_act": can_act,
    }
    return render(request, "negotiations/offer_detail.html", context)


@login_required
def offer_counter(request, offer_id):
    """Submit a counter-offer with revised price, quantity, or date."""
    offer = get_object_or_404(Offer, pk=offer_id)

    if request.user != offer.buyer and request.user != offer.crop_listing.farmer:
        messages.error(request, "Unauthorized to respond to this offer.")
        return redirect("dashboard")

    if offer.status not in [Offer.Status.PENDING, Offer.Status.COUNTERED]:
        messages.error(request, "This negotiation has already been concluded.")
        return redirect("offer_detail", offer_id=offer.id)

    if request.method == "POST":
        form = CounterOfferForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                msg = form.save(commit=False)
                msg.offer = offer
                msg.sender = request.user
                msg.recipient = offer.buyer if request.user == offer.crop_listing.farmer else offer.crop_listing.farmer
                msg.save()

                # Update offer terms if counter values were provided
                if msg.counter_price_per_kg:
                    offer.proposed_price_per_kg = msg.counter_price_per_kg
                if msg.counter_quantity_kg:
                    offer.quantity_kg = msg.counter_quantity_kg
                if msg.counter_delivery_date:
                    offer.delivery_date = msg.counter_delivery_date

                offer.status = Offer.Status.COUNTERED
                offer.current_turn = Offer.Turn.BUYER if request.user == offer.crop_listing.farmer else Offer.Turn.FARMER
                offer.save()

                AuditLog.log(
                    "COUNTER_OFFER",
                    "Offer",
                    offer.id,
                    f"{request.user.username} countered with ₹{offer.proposed_price_per_kg}/kg for {offer.quantity_kg}kg",
                    user=request.user
                )

                send_user_notification(
                    msg.recipient,
                    f"Counter-Offer on {offer.crop_listing.crop_name}",
                    f"{request.user.get_full_name() or request.user.username} submitted a counter-proposal: ₹{offer.proposed_price_per_kg}/kg for {offer.quantity_kg} kg.",
                    notification_type="COUNTER",
                    link_url=f"/negotiations/offers/{offer.id}/"
                )

                messages.success(request, "Your counter-offer has been recorded and the counterparty notified.")
    return redirect("offer_detail", offer_id=offer.id)


@login_required
def offer_accept(request, offer_id):
    """
    Accept the negotiated offer terms!
    Atomically creates a digital Contract proposal and reserves the crop stock.
    """
    offer = get_object_or_404(
        Offer.objects.select_related("crop_listing", "crop_listing__farmer", "buyer"),
        pk=offer_id
    )

    if request.user != offer.buyer and request.user != offer.crop_listing.farmer:
        messages.error(request, "Unauthorized action.")
        return redirect("dashboard")

    if offer.status not in [Offer.Status.PENDING, Offer.Status.COUNTERED]:
        messages.error(request, "Offer cannot be accepted in its current status.")
        return redirect("offer_detail", offer_id=offer.id)

    with transaction.atomic():
        crop = CropListing.objects.select_for_update().get(pk=offer.crop_listing.id)

        if crop.available_quantity_kg < offer.quantity_kg:
            messages.error(request, f"Insufficient stock: Available {crop.available_quantity_kg}kg, agreed {offer.quantity_kg}kg.")
            return redirect("offer_detail", offer_id=offer.id)

        # Reserve quantity
        crop.available_quantity_kg -= offer.quantity_kg
        if crop.available_quantity_kg <= 0:
            crop.status = CropListing.Status.RESERVED
        crop.save(update_fields=["available_quantity_kg", "status"])

        # Mark offer accepted
        offer.status = Offer.Status.ACCEPTED
        offer.current_turn = Offer.Turn.NONE
        offer.save(update_fields=["status", "current_turn"])

        # Create structured Contract
        contract_number = Contract.generate_contract_number()
        total_val = offer.quantity_kg * offer.proposed_price_per_kg

        contract = Contract.objects.create(
            contract_number=contract_number,
            offer=offer,
            farmer=offer.crop_listing.farmer,
            buyer=offer.buyer,
            crop_name=crop.crop_name,
            variety=crop.variety,
            quantity_kg=offer.quantity_kg,
            agreed_price_per_kg=offer.proposed_price_per_kg,
            total_value=total_val,
            delivery_location=offer.delivery_location,
            delivery_schedule=f"Target fulfillment on or before {offer.delivery_date.strftime('%d-%b-%Y')}.",
            quality_specifications=offer.quality_specifications or f"Standard {crop.quality_grade}. Compliance with FSSAI/AGMARK standards.",
            status=Contract.Status.PROPOSED
        )

        AuditLog.log(
            "OFFER_ACCEPTED",
            "Offer",
            offer.id,
            f"Offer #{offer.id} accepted by {request.user.username}. Contract {contract.contract_number} generated.",
            user=request.user
        )

        # Notify counterparty
        other_party = offer.buyer if request.user == offer.crop_listing.farmer else offer.crop_listing.farmer
        send_user_notification(
            other_party,
            f"Deal Agreed! Contract {contract.contract_number} Created",
            f"Both parties agreed to terms on {crop.crop_name}. Contract {contract.contract_number} is now ready for bilateral signoff.",
            notification_type="CONTRACT",
            link_url=f"/contracts/{contract.id}/"
        )

        messages.success(request, f"Congratulations! Agreement reached. Contract {contract.contract_number} has been drafted.")
        return redirect("contract_detail", contract_id=contract.id)


@login_required
def offer_reject(request, offer_id):
    """Reject an offer."""
    offer = get_object_or_404(Offer, pk=offer_id)
    if request.user != offer.buyer and request.user != offer.crop_listing.farmer:
        messages.error(request, "Unauthorized action.")
        return redirect("dashboard")

    offer.status = Offer.Status.REJECTED
    offer.current_turn = Offer.Turn.NONE
    offer.save(update_fields=["status", "current_turn"])

    other_party = offer.buyer if request.user == offer.crop_listing.farmer else offer.crop_listing.farmer
    send_user_notification(
        other_party,
        f"Offer Declined for {offer.crop_listing.crop_name}",
        f"{request.user.get_full_name() or request.user.username} declined the latest terms for Offer #{offer.id}.",
        notification_type="OFFER",
        link_url=f"/negotiations/offers/{offer.id}/"
    )

    messages.info(request, "Offer has been rejected.")
    return redirect("offer_detail", offer_id=offer.id)


@login_required
def offer_withdraw(request, offer_id):
    """Buyer withdraws their own offer."""
    offer = get_object_or_404(Offer, pk=offer_id, buyer=request.user)
    if offer.status in [Offer.Status.PENDING, Offer.Status.COUNTERED]:
        offer.status = Offer.Status.WITHDRAWN
        offer.current_turn = Offer.Turn.NONE
        offer.save(update_fields=["status", "current_turn"])
        messages.info(request, "Offer has been withdrawn.")
    return redirect("offer_detail", offer_id=offer.id)


@login_required
def api_offer_messages(request, offer_id):
    """JSON API endpoint for real-time polling / WebSocket fallback."""
    offer = get_object_or_404(Offer, pk=offer_id)
    if request.user != offer.buyer and request.user != offer.crop_listing.farmer and not request.user.is_platform_admin():
        return JsonResponse({"error": "Unauthorized"}, status=403)

    messages_qs = offer.messages.all().select_related("sender")
    data = []
    for m in messages_qs:
        data.append({
            "id": m.id,
            "sender_name": m.sender.get_full_name() or m.sender.username,
            "is_me": (m.sender == request.user),
            "message": m.message,
            "counter_price": str(m.counter_price_per_kg) if m.counter_price_per_kg else None,
            "counter_qty": str(m.counter_quantity_kg) if m.counter_quantity_kg else None,
            "created_at": m.created_at.strftime("%d-%b %H:%M"),
        })
    return JsonResponse({
        "status": offer.status,
        "current_price": str(offer.proposed_price_per_kg),
        "current_qty": str(offer.quantity_kg),
        "messages": data
    })
