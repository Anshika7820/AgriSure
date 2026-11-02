from django.db import models
from django.core.validators import MinValueValidator

class Delivery(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "SCHEDULED", "Scheduled"
        READY_FOR_DISPATCH = "READY_FOR_DISPATCH", "Harvested & Ready for Dispatch"
        IN_TRANSIT = "IN_TRANSIT", "In Transit"
        DELIVERED = "DELIVERED", "Delivered at Destination"
        CONFIRMED = "CONFIRMED", "Weighment & Quality Confirmed"
        REJECTED = "REJECTED", "Rejected / Quality Issue"

    contract = models.ForeignKey(
        "contracts.Contract",
        on_delete=models.PROTECT,
        related_name="deliveries"
    )
    delivery_number = models.CharField(max_length=50)
    scheduled_date = models.DateField()
    quantity_scheduled_kg = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    quantity_delivered_kg = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    quantity_received_kg = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Confirmed weight recorded by buyer after weighbridge scale"
    )
    dispatched_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    delivery_notes = models.TextField(blank=True, help_text="Vehicle info, driver phone, dispatch remarks")
    rejection_reason = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["scheduled_date", "created_at"]

    def __str__(self):
        return f"Delivery {self.delivery_number} ({self.contract.crop_name} - {self.quantity_scheduled_kg}kg) [{self.get_status_display()}]"
