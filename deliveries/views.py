from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from .models import Delivery
from .forms import DeliveryScheduleForm, DeliveryDispatchForm, DeliveryConfirmForm
from contracts.models import Contract
from payments.models import Payment
from notifications.services import send_user_notification
from audit.models import AuditLog

@login_required
def delivery_list(request):
    user = request.user
    if user.is_farmer():
        deliveries = Delivery.objects.filter(contract__farmer=user).select_related("contract", "contract__buyer")
    elif user.is_buyer():
        deliveries = Delivery.objects.filter(contract__buyer=user).select_related("contract", "contract__farmer")
    elif user.is_platform_admin():
        deliveries = Delivery.objects.all().select_related("contract", "contract__farmer", "contract__buyer")
    else:
        deliveries = Delivery.objects.none()

    status_filter = request.GET.get("status")
    if status_filter:
        deliveries = deliveries.filter(status=status_filter)

    return render(request, "deliveries/list.html", {"deliveries": deliveries, "current_status": status_filter})


@login_required
def delivery_detail(request, delivery_id):
    delivery = get_object_or_404(
        Delivery.objects.select_related("contract", "contract__farmer", "contract__buyer"),
        pk=delivery_id
    )

    if request.user != delivery.contract.farmer and request.user != delivery.contract.buyer and not request.user.is_platform_admin():
        messages.error(request, "Access restricted.")
        return redirect("dashboard")

    is_farmer = (request.user == delivery.contract.farmer)
    is_buyer = (request.user == delivery.contract.buyer)

    dispatch_form = DeliveryDispatchForm(instance=delivery)
    confirm_form = DeliveryConfirmForm(initial={"quantity_received_kg": delivery.quantity_delivered_kg or delivery.quantity_scheduled_kg})

    context = {
        "delivery": delivery,
        "is_farmer": is_farmer,
        "is_buyer": is_buyer,
        "dispatch_form": dispatch_form,
        "confirm_form": confirm_form,
    }
    return render(request, "deliveries/detail.html", context)


@login_required
def delivery_dispatch(request, delivery_id):
    delivery = get_object_or_404(Delivery, pk=delivery_id)
    if request.user != delivery.contract.farmer:
        messages.error(request, "Only the farmer can record dispatch.")
        return redirect("delivery_detail", delivery_id=delivery.id)

    if request.method == "POST":
        form = DeliveryDispatchForm(request.POST, instance=delivery)
        if form.is_valid():
            with transaction.atomic():
                deliv = form.save(commit=False)
                deliv.dispatched_at = timezone.now()
                deliv.status = Delivery.Status.IN_TRANSIT
                deliv.save()

                AuditLog.log("DELIVERY_DISPATCHED", "Delivery", deliv.id, f"Farmer dispatched {deliv.quantity_delivered_kg}kg of {delivery.contract.crop_name}", user=request.user)

                send_user_notification(
                    delivery.contract.buyer,
                    f"Consignment Dispatched: {delivery.delivery_number}",
                    f"Farmer dispatched {deliv.quantity_delivered_kg}kg for Contract {delivery.contract.contract_number}. Notes: {deliv.delivery_notes}",
                    notification_type="DELIVERY",
                    link_url=f"/deliveries/{deliv.id}/"
                )

                messages.success(request, f"Consignment {delivery.delivery_number} marked as IN TRANSIT.")
    return redirect("delivery_detail", delivery_id=delivery.id)


@login_required
def delivery_confirm(request, delivery_id):
    delivery = get_object_or_404(Delivery, pk=delivery_id)
    if request.user != delivery.contract.buyer:
        messages.error(request, "Only the buyer can record receipt confirmation.")
        return redirect("delivery_detail", delivery_id=delivery.id)

    if request.method == "POST":
        form = DeliveryConfirmForm(request.POST)
        if form.is_valid():
            decision = form.cleaned_data["decision"]
            received_qty = form.cleaned_data.get("quantity_received_kg") or delivery.quantity_delivered_kg or delivery.quantity_scheduled_kg
            reason = form.cleaned_data.get("rejection_reason", "")

            with transaction.atomic():
                if decision == "CONFIRM":
                    delivery.status = Delivery.Status.CONFIRMED
                    delivery.quantity_received_kg = received_qty
                    delivery.delivered_at = timezone.now()
                    delivery.save()

                    # Calculate milestone payable
                    milestone_amount = received_qty * delivery.contract.agreed_price_per_kg
                    Payment.objects.create(
                        contract=delivery.contract,
                        delivery=delivery,
                        payer=delivery.contract.buyer,
                        recipient=delivery.contract.farmer,
                        amount=milestone_amount,
                        payment_type=Payment.PaymentType.MILESTONE,
                        status=Payment.Status.PENDING,
                        notes=f"Payable for delivery batch {delivery.delivery_number} ({received_qty}kg @ ₹{delivery.contract.agreed_price_per_kg}/kg)"
                    )

                    AuditLog.log("DELIVERY_CONFIRMED", "Delivery", delivery.id, f"Buyer confirmed receipt of {received_qty}kg for Contract {delivery.contract.contract_number}", user=request.user)

                    send_user_notification(
                        delivery.contract.farmer,
                        f"Delivery Confirmed: {delivery.delivery_number}",
                        f"Buyer confirmed receipt of {received_qty}kg. Milestone payment of ₹{milestone_amount:,.2f} is generated.",
                        notification_type="DELIVERY",
                        link_url=f"/deliveries/{delivery.id}/"
                    )

                    # Check if total confirmed quantity fulfills contract
                    total_confirmed = Delivery.objects.filter(
                        contract=delivery.contract,
                        status=Delivery.Status.CONFIRMED
                    ).aggregate(total=Sum("quantity_received_kg"))["total"] or 0

                    if total_confirmed >= delivery.contract.quantity_kg:
                        delivery.contract.status = Contract.Status.COMPLETED
                        delivery.contract.save(update_fields=["status"])
                        send_user_notification(
                            delivery.contract.farmer,
                            f"Contract {delivery.contract.contract_number} FULFILLED!",
                            "All contracted volume has been delivered and verified. Contract completed!",
                            notification_type="CONTRACT",
                            link_url=f"/contracts/{delivery.contract.id}/"
                        )
                        send_user_notification(
                            delivery.contract.buyer,
                            f"Contract {delivery.contract.contract_number} FULFILLED!",
                            "All contracted volume delivered and verified. Please complete final settlement and leave a review.",
                            notification_type="CONTRACT",
                            link_url=f"/contracts/{delivery.contract.id}/"
                        )

                    messages.success(request, f"Delivery {delivery.delivery_number} confirmed! Milestone payment obligation created.")
                else:
                    delivery.status = Delivery.Status.REJECTED
                    delivery.rejection_reason = reason
                    delivery.delivered_at = timezone.now()
                    delivery.save()

                    AuditLog.log("DELIVERY_REJECTED", "Delivery", delivery.id, f"Buyer rejected delivery {delivery.delivery_number}. Reason: {reason}", user=request.user)

                    send_user_notification(
                        delivery.contract.farmer,
                        f"Delivery Rejected: {delivery.delivery_number}",
                        f"Buyer noted a rejection or discrepancy on delivery. Reason: {reason}",
                        notification_type="DELIVERY",
                        link_url=f"/deliveries/{delivery.id}/"
                    )
                    messages.warning(request, f"Delivery batch {delivery.delivery_number} has been rejected.")

    return redirect("delivery_detail", delivery_id=delivery.id)
