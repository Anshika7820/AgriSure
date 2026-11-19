from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import FileResponse, Http404
from django.utils import timezone
from .models import Contract, ContractAmendment
from .forms import ContractAmendmentForm, ContractSignForm
from .services import generate_contract_pdf
from deliveries.models import Delivery
from payments.models import Payment
from notifications.services import send_user_notification
from audit.models import AuditLog

@login_required
def contract_list(request):
    """Lists contracts associated with the logged-in user, filtered by status."""
    user = request.user
    if user.is_farmer():
        contracts = Contract.objects.filter(farmer=user).select_related("buyer")
    elif user.is_buyer():
        contracts = Contract.objects.filter(buyer=user).select_related("farmer")
    elif user.is_platform_admin():
        contracts = Contract.objects.all().select_related("farmer", "buyer")
    else:
        contracts = Contract.objects.none()

    status_filter = request.GET.get("status")
    if status_filter:
        contracts = contracts.filter(status=status_filter)

    return render(request, "contracts/list.html", {"contracts": contracts, "current_status": status_filter})


@login_required
def contract_detail(request, contract_id):
    """Comprehensive contract management page with status timeline, terms, signatures, deliveries, and payments."""
    contract = get_object_or_404(
        Contract.objects.select_related("farmer", "buyer", "offer", "offer__crop_listing"),
        pk=contract_id
    )

    if request.user != contract.farmer and request.user != contract.buyer and not request.user.is_platform_admin():
        messages.error(request, "Access restricted to contracted parties.")
        return redirect("dashboard")

    deliveries = contract.deliveries.all()
    payments = contract.payments.all()
    amendments = contract.amendments.all()
    disputes = contract.disputes.all()
    reviews = contract.reviews.all()

    is_farmer = (request.user == contract.farmer)
    is_buyer = (request.user == contract.buyer)

    user_has_signed = (is_farmer and contract.farmer_accepted) or (is_buyer and contract.buyer_accepted)
    can_sign = (contract.status in [Contract.Status.PROPOSED, Contract.Status.DRAFT]) and not user_has_signed

    sign_form = ContractSignForm()
    amendment_form = ContractAmendmentForm()

    context = {
        "contract": contract,
        "deliveries": deliveries,
        "payments": payments,
        "amendments": amendments,
        "disputes": disputes,
        "reviews": reviews,
        "is_farmer": is_farmer,
        "is_buyer": is_buyer,
        "user_has_signed": user_has_signed,
        "can_sign": can_sign,
        "sign_form": sign_form,
        "amendment_form": amendment_form,
    }
    return render(request, "contracts/detail.html", context)


@login_required
def contract_sign(request, contract_id):
    """Records authenticated digital signature for the contract."""
    contract = get_object_or_404(Contract, pk=contract_id)

    if request.user != contract.farmer and request.user != contract.buyer:
        messages.error(request, "Unauthorized to sign this contract.")
        return redirect("dashboard")

    if request.method == "POST":
        form = ContractSignForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                now = timezone.now()
                sig_hash = f"SIG-{request.user.role[:1]}-{request.user.id}-{int(now.timestamp())}"

                if request.user == contract.farmer:
                    contract.farmer_accepted = True
                    contract.farmer_accepted_at = now
                    contract.farmer_digital_signature = sig_hash
                    AuditLog.log("CONTRACT_SIGNED", "Contract", contract.id, f"Farmer {request.user.username} signed contract {contract.contract_number}", user=request.user)
                elif request.user == contract.buyer:
                    contract.buyer_accepted = True
                    contract.buyer_accepted_at = now
                    contract.buyer_digital_signature = sig_hash
                    AuditLog.log("CONTRACT_SIGNED", "Contract", contract.id, f"Buyer {request.user.username} signed contract {contract.contract_number}", user=request.user)

                # Check if both have signed to activate!
                was_activated = contract.check_and_activate()
                contract.save()

                if was_activated:
                    # Automatically schedule fulfillment delivery
                    delivery_date = contract.offer.delivery_date if contract.offer else (now.date() + timezone.timedelta(days=14))
                    Delivery.objects.create(
                        contract=contract,
                        delivery_number=f"DEL-{contract.contract_number}-01",
                        scheduled_date=delivery_date,
                        quantity_scheduled_kg=contract.quantity_kg,
                        delivery_notes="Initial scheduled fulfillment batch created upon bilateral contract signoff."
                    )

                    # Create advance deposit payment obligation (15% advance)
                    advance_amount = (contract.total_value * 15) / 100
                    Payment.objects.create(
                        contract=contract,
                        payer=contract.buyer,
                        recipient=contract.farmer,
                        amount=advance_amount,
                        payment_type=Payment.PaymentType.ADVANCE,
                        status=Payment.Status.PENDING,
                        notes=f"15% Advance booking deposit for Contract #{contract.contract_number}"
                    )

                    send_user_notification(
                        contract.farmer,
                        f"Contract {contract.contract_number} is Now ACTIVE!",
                        f"Both parties have executed digital signatures. Contract is active, delivery scheduled, and advance deposit created.",
                        notification_type="CONTRACT",
                        link_url=f"/contracts/{contract.id}/"
                    )
                    send_user_notification(
                        contract.buyer,
                        f"Contract {contract.contract_number} is Now ACTIVE!",
                        f"Both parties have executed digital signatures. Please initiate the advance booking deposit of ₹{advance_amount:,.2f}.",
                        notification_type="CONTRACT",
                        link_url=f"/contracts/{contract.id}/"
                    )

                    messages.success(request, f"Contract {contract.contract_number} has been fully signed and is now ACTIVE!")
                else:
                    other_party = contract.buyer if request.user == contract.farmer else contract.farmer
                    send_user_notification(
                        other_party,
                        f"Signature Received: Contract {contract.contract_number}",
                        f"{request.user.get_full_name() or request.user.username} has digitally signed the contract. Awaiting your counter-signature.",
                        notification_type="CONTRACT",
                        link_url=f"/contracts/{contract.id}/"
                    )
                    messages.success(request, "Your digital signature has been recorded. Awaiting counterparty signature to activate contract.")

    return redirect("contract_detail", contract_id=contract.id)


@login_required
def contract_amend(request, contract_id):
    """Proposes a formal amendment to an active or proposed contract."""
    contract = get_object_or_404(Contract, pk=contract_id)

    if request.user != contract.farmer and request.user != contract.buyer:
        messages.error(request, "Unauthorized action.")
        return redirect("dashboard")

    if request.method == "POST":
        form = ContractAmendmentForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                num = contract.amendments.count() + 1
                amendment = form.save(commit=False)
                amendment.contract = contract
                amendment.amendment_number = num
                amendment.proposed_by = request.user
                amendment.status = ContractAmendment.Status.PENDING
                amendment.save()

                AuditLog.log("AMENDMENT_PROPOSED", "ContractAmendment", amendment.id, f"Amendment #{num} proposed for contract {contract.contract_number}", user=request.user)

                other_party = contract.buyer if request.user == contract.farmer else contract.farmer
                send_user_notification(
                    other_party,
                    f"Contract Amendment Proposed: {contract.contract_number}",
                    f"{request.user.get_full_name() or request.user.username} proposed Amendment #{num} to terms. Please review.",
                    notification_type="CONTRACT",
                    link_url=f"/contracts/{contract.id}/"
                )

                messages.success(request, f"Amendment #{num} proposed and sent for counterparty approval.")
    return redirect("contract_detail", contract_id=contract.id)


@login_required
def contract_amend_respond(request, contract_id, amendment_id):
    """Approve or reject a contract amendment."""
    contract = get_object_or_404(Contract, pk=contract_id)
    amendment = get_object_or_404(ContractAmendment, pk=amendment_id, contract=contract)

    if request.user == amendment.proposed_by:
        messages.error(request, "You cannot review your own proposed amendment.")
        return redirect("contract_detail", contract_id=contract.id)

    decision = request.POST.get("decision")
    if decision == "ACCEPT":
        with transaction.atomic():
            amendment.status = ContractAmendment.Status.ACCEPTED
            amendment.save()

            if amendment.adjusted_quantity_kg:
                contract.quantity_kg = amendment.adjusted_quantity_kg
            if amendment.adjusted_price_per_kg:
                contract.agreed_price_per_kg = amendment.adjusted_price_per_kg

            contract.total_value = contract.quantity_kg * contract.agreed_price_per_kg
            contract.save()

            AuditLog.log("AMENDMENT_ACCEPTED", "ContractAmendment", amendment.id, f"Amendment #{amendment.amendment_number} accepted for contract {contract.contract_number}", user=request.user)

            send_user_notification(
                amendment.proposed_by,
                f"Amendment Accepted for {contract.contract_number}",
                f"Your proposed Amendment #{amendment.amendment_number} was approved and contract terms updated.",
                notification_type="CONTRACT",
                link_url=f"/contracts/{contract.id}/"
            )
            messages.success(request, f"Amendment #{amendment.amendment_number} accepted and integrated into active contract.")
    elif decision == "REJECT":
        amendment.status = ContractAmendment.Status.REJECTED
        amendment.save()
        messages.info(request, f"Amendment #{amendment.amendment_number} rejected.")

    return redirect("contract_detail", contract_id=contract.id)


@login_required
def contract_download_pdf(request, contract_id):
    """Generates and serves downloadable PDF contract document."""
    contract = get_object_or_404(Contract, pk=contract_id)

    if request.user != contract.farmer and request.user != contract.buyer and not request.user.is_platform_admin():
        raise Http404("Document access restricted.")

    pdf_buffer = generate_contract_pdf(contract)
    filename = f"AgriSure_Contract_{contract.contract_number}.pdf"

    return FileResponse(pdf_buffer, as_attachment=True, filename=filename, content_type="application/pdf")
