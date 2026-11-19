from django.contrib import admin
from .models import CropCategory, CropListing

@admin.register(CropCategory)
class CropCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "icon")

@admin.register(CropListing)
class CropListingAdmin(admin.ModelAdmin):
    list_display = ("crop_name", "variety", "farmer", "total_quantity_kg", "available_quantity_kg", "expected_price_per_kg", "status", "created_at")
    list_filter = ("status", "category")
    search_fields = ("crop_name", "variety", "farmer__username")
