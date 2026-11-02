from django.contrib import admin
from .models import Farm

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ("farm_name", "farmer", "district", "state", "area_acres", "created_at")
    search_fields = ("farm_name", "farmer__username", "district")
