from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Payment Due / Pending"
        PROCESSING = "PROCESSING", "Processing at Gateway"
        SUCCESS = "SUCCESS", "Settled / Successful"
        FAILED = "FAILED", "Failed"
        REFUNDED = "REFUNDED", "Refunded"

    class PaymentType(models.TextChoices):
        ADVANCE = "ADVANCE", "Advance Security Deposit"
        MILESTONE = "MILESTONE", "Delivery Batch Fulfillment"
        FINAL = "FINAL", "Final Settlement Balance"

    contract = models.ForeignKey(
        "contracts.Contract",
        on_delete=models.PROTECT,
        related_name="payments"
    )
    delivery = models.ForeignKey(
        "deliveries.Delivery",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments"
    )
    payer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="payments_made"
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="payments_received"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(1.0)]
    )
    currency = models.CharField(max_length=3, default="INR")
    payment_type = models.CharField(
        max_length=15,
        choices=PaymentType.choices,
        default=PaymentType.MILESTONE
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING
    )
    payment_method = models.CharField(
        max_length=50,
        default="Direct Bank Transfer / Escrow UPI"
    )
    gateway_order_id = models.CharField(max_length=100, blank=True)
    gateway_payment_id = models.CharField(max_length=100, blank=True)
    gateway_signature = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Payment #{self.id} for {self.contract.contract_number}: ₹{self.amount:,.2f} [{self.get_status_display()}]"
