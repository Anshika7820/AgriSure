from django.db import models
from django.conf import settings

class Dispute(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Grievance Raised / Open"
        UNDER_REVIEW = "UNDER_REVIEW", "Under Platform Conciliation"
        RESOLVED = "RESOLVED", "Mutually Resolved"
        REJECTED = "REJECTED", "Dismissed / Unsubstantiated"

    class ReasonCategory(models.TextChoices):
        QUALITY = "QUALITY", "Produce Quality Below Agreed Specifications"
        WEIGHT = "WEIGHT", "Discrepancy in Quantity / Weighbridge Weight"
        DELIVERY_DELAY = "DELIVERY_DELAY", "Delayed Dispatch or Non-Delivery"
        PAYMENT_DELAY = "PAYMENT_DELAY", "Delayed Milestone or Final Settlement"
        BREACH_TERMS = "BREACH_TERMS", "Unilateral Terms Modification"
        OTHER = "OTHER", "Other Supply Chain Grievance"

    contract = models.ForeignKey(
        "contracts.Contract",
        on_delete=models.PROTECT,
        related_name="disputes"
    )
    raised_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="disputes_raised"
    )
    reason = models.CharField(
        max_length=50,
        choices=ReasonCategory.choices,
        default=ReasonCategory.QUALITY
    )
    description = models.TextField(help_text="Provide clear details and facts regarding the dispute")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN
    )
    assigned_admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_disputes"
    )
    resolution_notes = models.TextField(blank=True, help_text="Official platform mediator findings and directions")
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Dispute #{self.id} on {self.contract.contract_number} by {self.raised_by.username} [{self.get_status_display()}]"
