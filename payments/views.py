from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import FileResponse, Http404
from django.utils import timezone
from django.conf import settings
import hashlib
import hmac
from .models import Payment
from .services import generate_payment_receipt_pdf, verify_mock_or_razorpay_signature
from notifications.services import send_user_notification
from audit.models import AuditLog

@login_required
def payment_list(request):
    user = request.user
    if user.is_farmer():
        payments = Payment.objects.filter(recipient=user).select_related("contract", "payer")
    elif user.is_buyer():
        payments = Payment.objects.filter(payer=user).select_related("contract", "recipient")
    elif user.is_platform_admin():
        payments = Payment.objects.all().select_related("contract", "payer", "recipient")
    else:
        payments = Payment.objects.none()

    status_filter = request.GET.get("status")
    if status_filter:
        payments = payments.filter(status=status_filter)

    return render(request, "payments/list.html", {"payments": payments, "current_status": status_filter})


@login_required
def payment_detail(request, payment_id):
    payment = get_object_or_404(
        Payment.objects.select_related("contract", "payer", "recipient"),
        pk=payment_id
    )

    if request.user != payment.payer and request.user != payment.recipient and not request.user.is_platform_admin():
        messages.error(request, "Unauthorized access.")
        return redirect("dashboard")

    is_payer = (request.user == payment.payer)

    return render(request, "payments/detail.html", {"payment": payment, "is_payer": is_payer})


@login_required
def payment_checkout(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id, payer=request.user)

    if payment.status == Payment.Status.SUCCESS:
        messages.info(request, "This payment obligation has already been settled.")
        return redirect("payment_detail", payment_id=payment.id)

    if request.method == "POST":
        method = request.POST.get("payment_method", "Razorpay Test Gateway")
        pay_id = request.POST.get("razorpay_payment_id") or f"pay_test_{int(timezone.now().timestamp())}"
        order_id = request.POST.get("razorpay_order_id") or f"order_test_{payment.id}_{int(timezone.now().timestamp())}"
        signature = request.POST.get("razorpay_signature") or f"rzp_sig_{hashlib.sha256((order_id + pay_id).encode()).hexdigest()[:20]}"

        # Server-side verification
        if verify_mock_or_razorpay_signature(order_id, pay_id, signature):
            with transaction.atomic():
                payment.status = Payment.Status.SUCCESS
                payment.payment_method = method
                payment.gateway_order_id = order_id
                payment.gateway_payment_id = pay_id
                payment.gateway_signature = signature
                payment.paid_at = timezone.now()
                payment.save()

                AuditLog.log(
                    "PAYMENT_SUCCESS",
                    "Payment",
                    payment.id,
                    f"Settled payment of ₹{payment.amount:,.2f} via {method} for Contract {payment.contract.contract_number} (Ref: {pay_id})",
                    user=request.user
                )

                # Send notifications
                send_user_notification(
                    payment.recipient,
                    f"Payment Received: ₹{payment.amount:,.2f}",
                    f"Buyer transferred ₹{payment.amount:,.2f} for Contract {payment.contract.contract_number} ({payment.get_payment_type_display()}).",
                    notification_type="PAYMENT",
                    link_url=f"/payments/{payment.id}/"
                )
                send_user_notification(
                    payment.payer,
                    f"Payment Confirmed: ₹{payment.amount:,.2f}",
                    f"Your payment of ₹{payment.amount:,.2f} for Contract {payment.contract.contract_number} has been verified and settled via Razorpay Test Gateway.",
                    notification_type="PAYMENT",
                    link_url=f"/payments/{payment.id}/"
                )

                messages.success(request, f"Payment of ₹{payment.amount:,.2f} successfully processed via Razorpay Test Mode! Reference: {pay_id}")
                return redirect("payment_detail", payment_id=payment.id)
        else:
            payment.status = Payment.Status.FAILED
            payment.save(update_fields=["status"])
            messages.error(request, "Payment signature verification failed. Please try again.")

    razorpay_key_id = getattr(settings, "RAZORPAY_KEY_ID", "rzp_test_AgriSureFarming2026")
    amount_paise = int(payment.amount * 100)

    context = {
        "payment": payment,
        "razorpay_key_id": razorpay_key_id,
        "amount_paise": amount_paise,
    }
    return render(request, "payments/checkout.html", context)


@login_required
def payment_receipt_download(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)

    if request.user != payment.payer and request.user != payment.recipient and not request.user.is_platform_admin():
        raise Http404("Document access restricted.")

    if payment.status != Payment.Status.SUCCESS:
        messages.error(request, "Receipt is only available for successful settled transactions.")
        return redirect("payment_detail", payment_id=payment.id)

    pdf_buffer = generate_payment_receipt_pdf(payment)
    filename = f"AgriSure_Receipt_TXN_{payment.id:06d}.pdf"
    return FileResponse(pdf_buffer, as_attachment=True, filename=filename, content_type="application/pdf")
