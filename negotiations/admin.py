from django.contrib import admin
from .models import Offer, NegotiationMessage

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("id", "crop_listing", "buyer", "quantity_kg", "proposed_price_per_kg", "status", "current_turn", "created_at")
    list_filter = ("status", "current_turn")

@admin.register(NegotiationMessage)
class NegotiationMessageAdmin(admin.ModelAdmin):
    list_display = ("offer", "sender", "recipient", "counter_price_per_kg", "counter_quantity_kg", "created_at")
