from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class CropCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default="bi-flower1", help_text="Bootstrap icon class")

    class Meta:
        verbose_name_plural = "Crop Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class CropListing(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        ACTIVE = "ACTIVE", "Active / Available"
        RESERVED = "RESERVED", "Reserved / Under Contract"
        CLOSED = "CLOSED", "Closed / Harvested"

    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="crop_listings"
    )
    farm = models.ForeignKey(
        "farms.Farm",
        on_delete=models.PROTECT,
        related_name="crop_listings"
    )
    category = models.ForeignKey(
        CropCategory,
        on_delete=models.PROTECT,
        related_name="listings"
    )
    crop_name = models.CharField(max_length=150)
    variety = models.CharField(max_length=100, blank=True)
    total_quantity_kg = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Expected harvest yield in kilograms"
    )
    available_quantity_kg = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
        help_text="Remaining available quantity for contract"
    )
    expected_price_per_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Base/expected price in INR (₹) per kg"
    )
    quality_grade = models.CharField(
        max_length=50,
        default="Grade A (Standard)",
        help_text="e.g. Grade A, Organic Certified, Export Grade"
    )
    expected_harvest_date = models.DateField(help_text="Estimated date when crop will be ready")
    available_from = models.DateField(help_text="Earliest delivery dispatch date")
    crop_image = models.ImageField(upload_to="crops/", null=True, blank=True)
    description = models.TextField(blank=True, help_text="Agronomic practices, pesticide usage, specifications")
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.ACTIVE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def total_potential_value(self):
        return self.total_quantity_kg * self.expected_price_per_kg

    def __str__(self):
        return f"{self.crop_name} ({self.variety or 'Standard'}) - {self.available_quantity_kg}kg available"
