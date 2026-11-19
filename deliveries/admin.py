from django.contrib import admin
from .models import Delivery

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ("delivery_number", "contract", "scheduled_date", "quantity_scheduled_kg", "quantity_received_kg", "status")
    list_filter = ("status", "scheduled_date")
