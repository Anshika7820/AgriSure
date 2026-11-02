from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "user", "action", "object_type", "object_id", "summary")
    list_filter = ("action", "object_type")
    search_fields = ("summary", "user__username", "object_id")
