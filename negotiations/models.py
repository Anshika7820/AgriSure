from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class Offer(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending Farmer Response"
        COUNTERED = "COUNTERED", "Counter-Offer Active"
        ACCEPTED = "ACCEPTED", "Accepted / Ready for Contract"
        REJECTED = "REJECTED", "Rejected"
        WITHDRAWN = "WITHDRAWN", "Withdrawn by Buyer"

    class Turn(models.TextChoices):
        FARMER = "FARMER", "Awaiting Farmer"
        BUYER = "BUYER", "Awaiting Buyer"
        NONE = "NONE", "Concluded"

    crop_listing = models.ForeignKey(
        "marketplace.CropListing",
        on_delete=models.PROTECT,
        related_name="offers"
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="offers_made"
    )
    quantity_kg = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(1.0)],
        help_text="Requested purchase volume in kilograms"
    )
    proposed_price_per_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Agreed/proposed rate in ₹/kg"
    )
    delivery_date = models.DateField(help_text="Desired fulfillment date")
    delivery_location = models.CharField(max_length=255, help_text="Delivery warehouse / destination")
    quality_specifications = models.TextField(blank=True, help_text="Specific moisture, purity, or packing criteria")
    message = models.TextField(blank=True, help_text="Initial proposal note")
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING
    )
    current_turn = models.CharField(
        max_length=10,
        choices=Turn.choices,
        default=Turn.FARMER
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    @property
    def total_offer_value(self):
        return self.quantity_kg * self.proposed_price_per_kg

    def __str__(self):
        return f"Offer #{self.id} for {self.crop_listing.crop_name} by {self.buyer.username} (₹{self.proposed_price_per_kg}/kg)"


class NegotiationMessage(models.Model):
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_negotiations"
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_negotiations"
    )
    message = models.TextField(help_text="Negotiation note or term explanation")
    counter_price_per_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Revised counter-offer rate per kg, if modified"
    )
    counter_quantity_kg = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Revised quantity in kg, if modified"
    )
    counter_delivery_date = models.DateField(
        null=True,
        blank=True,
        help_text="Revised delivery schedule, if modified"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Msg from {self.sender.username} on Offer #{self.offer_id} at {self.created_at.strftime('%d-%b %H:%M')}"
