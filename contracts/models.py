from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

class Contract(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PROPOSED = "PROPOSED", "Pending Bilateral Signoff"
        ACCEPTED = "ACCEPTED", "Accepted (Ready for Execution)"
        ACTIVE = "ACTIVE", "Active / In Progress"
        COMPLETED = "COMPLETED", "Fulfilled & Completed"
        CANCELLED = "CANCELLED", "Cancelled"
        DISPUTED = "DISPUTED", "Under Dispute"

    contract_number = models.CharField(max_length=50, unique=True, db_index=True)
    offer = models.OneToOneField(
        "negotiations.Offer",
        on_delete=models.PROTECT,
        related_name="contract"
    )
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="farmer_contracts"
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="buyer_contracts"
    )
    crop_name = models.CharField(max_length=150)
    variety = models.CharField(max_length=100, blank=True)
    quantity_kg = models.DecimalField(max_digits=12, decimal_places=2)
    agreed_price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    total_value = models.DecimalField(max_digits=12, decimal_places=2)

    quality_specifications = models.TextField(
        default="Produce must comply with Indian Agricultural Standards (AGMARK Grade A). Maximum permissible moisture: 12%. Foreign matter under 1.5%."
    )
    delivery_schedule = models.TextField(
        help_text="Deliveries to be completed on or before agreed date with reasonable transit allowances."
    )
    delivery_location = models.CharField(max_length=255)
    payment_terms = models.TextField(
        default="15% Advance booking deposit upon contract activation, 85% balance released within 48 hours of verified batch weighment and quality confirmation."
    )
    inspection_terms = models.TextField(
        default="Joint inspection at buyer's designated collection center / warehouse within 24 hours of delivery. Rejection requires objective testing report."
    )
    cancellation_terms = models.TextField(
        default="Force majeure (unavoidable extreme climate events) allows mutually renegotiated timelines. Arbitrary breach incurs dispute settlement penalty."
    )
    dispute_procedure = models.TextField(
        default="Both parties agree to submit grievances to the AgriSure Platform Dispute Resolution Conciliation Tribunal before pursuing external statutory remedies."
    )

    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PROPOSED
    )

    # Bilateral acceptance tracking
    farmer_accepted = models.BooleanField(default=False)
    farmer_accepted_at = models.DateTimeField(null=True, blank=True)
    farmer_digital_signature = models.CharField(max_length=255, blank=True)

    buyer_accepted = models.BooleanField(default=False)
    buyer_accepted_at = models.DateTimeField(null=True, blank=True)
    buyer_digital_signature = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    @classmethod
    def generate_contract_number(cls):
        year = timezone.now().year
        uid = uuid.uuid4().hex[:6].upper()
        return f"AGRI-{year}-{uid}"

    def check_and_activate(self):
        """Activates contract when both farmer and buyer have signed/accepted."""
        if self.farmer_accepted and self.buyer_accepted:
            if self.status in [self.Status.PROPOSED, self.Status.DRAFT, self.Status.ACCEPTED]:
                self.status = self.Status.ACTIVE
                self.save(update_fields=["status"])
                return True
        return False

    @property
    def is_fully_signed(self):
        return self.farmer_accepted and self.buyer_accepted

    def __str__(self):
        return f"Contract {self.contract_number} ({self.crop_name} - ₹{self.total_value:,.2f})"


class ContractAmendment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending Counterparty Approval"
        ACCEPTED = "ACCEPTED", "Accepted & Integrated"
        REJECTED = "REJECTED", "Rejected"

    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name="amendments"
    )
    amendment_number = models.PositiveIntegerField(default=1)
    proposed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="proposed_amendments"
    )
    description = models.TextField(help_text="Detailed reason for schedule or volume adjustment")
    adjusted_quantity_kg = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    adjusted_price_per_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Amendment #{self.amendment_number} for {self.contract.contract_number}"
