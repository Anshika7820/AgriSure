from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Dispute
from .forms import DisputeForm, DisputeResolveForm
from contracts.models import Contract
from notifications.services import send_user_notification
from audit.models import AuditLog

@login_required
def dispute_list(request):
    user = request.user
    if user.is_platform_admin():
        disputes = Dispute.objects.all().select_related("contract", "raised_by")
    else:
        disputes = Dispute.objects.filter(
            contract__in=Contract.objects.filter(farmer=user) | Contract.objects.filter(buyer=user)
        ).select_related("contract", "raised_by")

    return render(request, "disputes/list.html", {"disputes": disputes})


@login_required
def dispute_create(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)

    if request.user != contract.farmer and request.user != contract.buyer:
        messages.error(request, "You can only raise a dispute for your own contracts.")
        return redirect("dashboard")

    if request.method == "POST":
        form = DisputeForm(request.POST)
        if form.is_valid():
            dispute = form.save(commit=False)
            dispute.contract = contract
            dispute.raised_by = request.user
            dispute.status = Dispute.Status.OPEN
            dispute.save()

            # Mark contract status
            contract.status = Contract.Status.DISPUTED
            contract.save(update_fields=["status"])

            AuditLog.log("DISPUTE_RAISED", "Dispute", dispute.id, f"Dispute #{dispute.id} raised on Contract {contract.contract_number} by {request.user.username}", user=request.user)

            other_party = contract.buyer if request.user == contract.farmer else contract.farmer
            send_user_notification(
                other_party,
                f"Dispute Notice: Contract {contract.contract_number}",
                f"{request.user.get_full_name() or request.user.username} raised a formal grievance: {dispute.get_reason_display()}.",
                notification_type="DISPUTE",
                link_url=f"/disputes/{dispute.id}/"
            )

            messages.warning(request, f"Formal dispute #{dispute.id} has been submitted for platform conciliation.")
            return redirect("dispute_detail", dispute_id=dispute.id)
    else:
        form = DisputeForm()

    return render(request, "disputes/create.html", {"form": form, "contract": contract})


@login_required
def dispute_detail(request, dispute_id):
    dispute = get_object_or_404(
        Dispute.objects.select_related("contract", "contract__farmer", "contract__buyer", "raised_by"),
        pk=dispute_id
    )

    if request.user != dispute.contract.farmer and request.user != dispute.contract.buyer and not request.user.is_platform_admin():
        messages.error(request, "Unauthorized access.")
        return redirect("dashboard")

    is_admin = request.user.is_platform_admin()
    resolve_form = DisputeResolveForm(instance=dispute) if is_admin else None

    context = {
        "dispute": dispute,
        "is_admin": is_admin,
        "resolve_form": resolve_form,
    }
    return render(request, "disputes/detail.html", context)


@login_required
def dispute_resolve(request, dispute_id):
    if not request.user.is_platform_admin():
        messages.error(request, "Only platform administrators can resolve formal disputes.")
        return redirect("dashboard")

    dispute = get_object_or_404(Dispute, pk=dispute_id)
    if request.method == "POST":
        form = DisputeResolveForm(request.POST, instance=dispute)
        if form.is_valid():
            disp = form.save(commit=False)
            disp.assigned_admin = request.user
            disp.resolved_at = timezone.now()
            disp.save()

            if disp.status == Dispute.Status.RESOLVED:
                disp.contract.status = Contract.Status.ACTIVE
                disp.contract.save(update_fields=["status"])

            AuditLog.log("DISPUTE_RESOLVED", "Dispute", disp.id, f"Admin {request.user.username} resolved Dispute #{disp.id} as {disp.get_status_display()}", user=request.user)

            # Notify both parties
            for party in [disp.contract.farmer, disp.contract.buyer]:
                send_user_notification(
                    party,
                    f"Dispute #{disp.id} Resolution Issued",
                    f"Platform arbitrator recorded findings: {disp.get_status_display()}.",
                    notification_type="DISPUTE",
                    link_url=f"/disputes/{disp.id}/"
                )

            messages.success(request, f"Dispute #{disp.id} status updated to {disp.get_status_display()}.")
    return redirect("dispute_detail", dispute_id=dispute.id)
