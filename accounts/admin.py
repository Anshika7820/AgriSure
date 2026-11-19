from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, FarmerProfile, BuyerProfile, VerificationDocument

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "phone", "is_verified", "is_staff")
    list_filter = ("role", "is_verified", "is_staff", "is_active")
    fieldsets = UserAdmin.fieldsets + (
        ("AgriSure Profile", {"fields": ("role", "phone", "is_verified")}),
    )

@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "farm_name", "village", "district", "state", "farm_area_acres")
    search_fields = ("user__username", "farm_name", "district")

@admin.register(BuyerProfile)
class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "business_name", "business_type", "district", "state", "registration_number")
    search_fields = ("user__username", "business_name", "registration_number")

@admin.register(VerificationDocument)
class VerificationDocumentAdmin(admin.ModelAdmin):
    list_display = ("user", "document_type", "status", "submitted_at", "reviewed_at")
    list_filter = ("status", "document_type")
