from django.db import models
from django.conf import settings

class Farm(models.Model):
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="farms"
    )
    farm_name = models.CharField(max_length=150)
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=12, blank=True)
    area_acres = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Cultivable area in acres"
    )
    soil_type = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g. Alluvial, Black Soil, Red Soil, Clayey Loam"
    )
    irrigation_source = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g. Tube well, Canal, Drip Irrigation, Rainfed"
    )
    survey_number = models.CharField(
        max_length=50,
        blank=True,
        help_text="Khasra / Survey Number"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.farm_name} ({self.district}, {self.state}) - {self.area_acres} Acres"
