from django.contrib import admin
from .models import Contract, ContractAmendment

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("contract_number", "crop_name", "farmer", "buyer", "quantity_kg", "total_value", "status", "farmer_accepted", "buyer_accepted")
    list_filter = ("status", "farmer_accepted", "buyer_accepted")
    search_fields = ("contract_number", "farmer__username", "buyer__username", "crop_name")

@admin.register(ContractAmendment)
class ContractAmendmentAdmin(admin.ModelAdmin):
    list_display = ("contract", "amendment_number", "proposed_by", "status", "created_at")
