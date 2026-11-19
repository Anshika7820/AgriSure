from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from accounts.decorators import admin_required
from accounts.models import User, VerificationDocument
from marketplace.models import CropListing
from contracts.models import Contract
from disputes.models import Dispute
from payments.models import Payment
from .models import AuditLog
from notifications.services import send_user_notification

@admin_required
def admin_dashboard(request):
    """Main administrative operations dashboard for platform compliance and governance."""
    total_users = User.objects.count()
    total_farmers = User.objects.filter(role=User.Role.FARMER).count()
    total_buyers = User.objects.filter(role=User.Role.BUYER).count()

    pending_verifications = VerificationDocument.objects.filter(status=VerificationDocument.Status.PENDING).count()
    active_crops = CropListing.objects.filter(status=CropListing.Status.ACTIVE).count()
    active_contracts = Contract.objects.filter(status=Contract.Status.ACTIVE).count()
    open_disputes = Dispute.objects.filter(status__in=[Dispute.Status.OPEN, Dispute.Status.UNDER_REVIEW]).count()

    recent_audits = AuditLog.objects.all()[:10]
    recent_verifications = VerificationDocument.objects.filter(status=VerificationDocument.Status.PENDING).select_related("user")[:5]
    recent_disputes = Dispute.objects.filter(status=Dispute.Status.OPEN).select_related("contract", "raised_by")[:5]

    context = {
        "total_users": total_users,
        "total_farmers": total_farmers,
        "total_buyers": total_buyers,
        "pending_verifications": pending_verifications,
        "active_crops": active_crops,
        "active_contracts": active_contracts,
        "open_disputes": open_disputes,
        "recent_audits": recent_audits,
        "recent_verifications": recent_verifications,
        "recent_disputes": recent_disputes,
    }
    return render(request, "admin_dashboard/dashboard.html", context)


@admin_required
def admin_verifications_list(request):
    """Review farmer land records and buyer business licenses."""
    documents = VerificationDocument.objects.all().select_related("user").order_by("-submitted_at")
    status_filter = request.GET.get("status")
    if status_filter:
        documents = documents.filter(status=status_filter)

    return render(request, "admin_dashboard/verifications.html", {"documents": documents, "status_filter": status_filter})


@admin_required
def admin_verify_action(request, doc_id):
    """Approve or reject verification document."""
    doc = get_object_or_404(VerificationDocument, pk=doc_id)
    action = request.POST.get("action")
    notes = request.POST.get("admin_notes", "")

    if action == "APPROVE":
        doc.status = VerificationDocument.Status.APPROVED
        doc.admin_notes = notes
        doc.reviewed_at = timezone.now()
        doc.save()

        # Update user is_verified status
        user = doc.user
        user.is_verified = True
        user.save(update_fields=["is_verified"])

        AuditLog.log("VERIFICATION_APPROVED", "VerificationDocument", doc.id, f"Approved {doc.document_type} for {user.username}", user=request.user)

        send_user_notification(
            user,
            "Verification Approved!",
            f"Your {doc.document_type} has been reviewed and verified. Your AgriSure account now has a Verified Badge.",
            notification_type="SYSTEM",
            link_url="/profile/"
        )
        messages.success(request, f"Document approved! User {user.username} is now verified.")
    elif action == "REJECT":
        doc.status = VerificationDocument.Status.REJECTED
        doc.admin_notes = notes
        doc.reviewed_at = timezone.now()
        doc.save()

        AuditLog.log("VERIFICATION_REJECTED", "VerificationDocument", doc.id, f"Rejected {doc.document_type} for {doc.user.username}. Reason: {notes}", user=request.user)

        send_user_notification(
            doc.user,
            "Verification Document Update",
            f"Your {doc.document_type} requires revision. Reason: {notes}",
            notification_type="SYSTEM",
            link_url="/profile/"
        )
        messages.warning(request, f"Document rejected for {doc.user.username}.")

    return redirect("admin_verifications")


@admin_required
def admin_users_list(request):
    """Platform user management with account status toggles."""
    users = User.objects.all().order_by("-date_joined")
    role_filter = request.GET.get("role")
    if role_filter:
        users = users.filter(role=role_filter)

    return render(request, "admin_dashboard/users.html", {"users": users, "role_filter": role_filter})


@admin_required
def admin_user_toggle_active(request, user_id):
    """Suspend or reactivate user account."""
    target_user = get_object_or_404(User, pk=user_id)
    if target_user.is_superuser:
        messages.error(request, "Cannot modify superuser status.")
        return redirect("admin_users")

    target_user.is_active = not target_user.is_active
    target_user.save(update_fields=["is_active"])

    status_str = "Reactivated" if target_user.is_active else "Suspended"
    AuditLog.log("USER_STATUS_CHANGE", "User", target_user.id, f"Admin {request.user.username} {status_str} account {target_user.username}", user=request.user)
    messages.info(request, f"User {target_user.username} has been {status_str}.")
    return redirect("admin_users")


@admin_required
def admin_audit_logs(request):
    """Audit log viewer."""
    logs = AuditLog.objects.all().select_related("user").order_by("-timestamp")
    return render(request, "admin_dashboard/audit_logs.html", {"logs": logs})
