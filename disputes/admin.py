from django.contrib import admin
from .models import Dispute

@admin.register(Dispute)
class DisputeAdmin(admin.ModelAdmin):
    list_display = ("id", "contract", "raised_by", "reason", "status", "created_at", "resolved_at")
    list_filter = ("status", "reason")
