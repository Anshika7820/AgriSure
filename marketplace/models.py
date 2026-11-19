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

    def get_default_image_path(self):
        name_lower = (self.crop_name or "").lower()
        cat_lower = (self.category.name if self.category else "").lower()
        if "wheat" in name_lower or "grain" in name_lower:
            return "crops/sharbati_premium_wheat.jpg"
        elif "rice" in name_lower or "basmati" in name_lower or "paddy" in name_lower:
            return "crops/traditional_basmati_rice_1121.jpg"
        elif "cotton" in name_lower or "fiber" in cat_lower:
            return "crops/organic_bt_cotton_(long_staple).jpg"
        elif "mustard" in name_lower or "oil" in cat_lower or "oilseed" in cat_lower:
            return "crops/yellow_mustard_(pusa_bold).jpg"
        elif "turmeric" in name_lower or "haldi" in name_lower:
            return "crops/salem_turmeric_fingers.jpg"
        elif "chilli" in name_lower or "chili" in name_lower or "mirch" in name_lower:
            return "crops/guntur_teja_red_chilli.jpg"
        elif "pepper" in name_lower:
            return "crops/malabar_black_pepper.jpg"
        elif "mango" in name_lower:
            return "crops/ratnagiri_alphonso_mangoes.jpg"
        elif "apple" in name_lower:
            return "crops/shimla_royal_delicious_apples.jpg"
        elif "chickpea" in name_lower or "chana" in name_lower or "pulse" in cat_lower or "dal" in name_lower or "legume" in cat_lower:
            return "crops/organic_desi_chickpeas.jpg"
        elif "fruit" in cat_lower or "horticulture" in cat_lower:
            return "crops/ratnagiri_alphonso_mangoes.jpg"
        elif "spice" in cat_lower:
            return "crops/salem_turmeric_fingers.jpg"
        return "crops/sharbati_premium_wheat.jpg"

    def save(self, *args, **kwargs):
        if not self.crop_image:
            self.crop_image = self.get_default_image_path()
        super().save(*args, **kwargs)

    @property
    def image_url(self):
        if self.crop_image and hasattr(self.crop_image, 'url'):
            try:
                return self.crop_image.url
            except ValueError:
                pass
        return f"/media/{self.get_default_image_path()}"

    @property
    def total_potential_value(self):
        return self.total_quantity_kg * self.expected_price_per_kg

    def __str__(self):
        return f"{self.crop_name} ({self.variety or 'Standard'}) - {self.available_quantity_kg}kg available"
