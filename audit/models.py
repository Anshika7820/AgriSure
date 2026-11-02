from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_actions"
    )
    action = models.CharField(max_length=100, help_text="e.g. OFFER_ACCEPTED, CONTRACT_SIGNED, PAYMENT_VERIFIED")
    object_type = models.CharField(max_length=100)
    object_id = models.CharField(max_length=50)
    summary = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    @classmethod
    def log(cls, action, object_type, object_id, summary, user=None, ip_address=None):
        return cls.objects.create(
            user=user,
            action=action,
            object_type=object_type,
            object_id=str(object_id),
            summary=summary,
            ip_address=ip_address
        )

    def __str__(self):
        actor = self.user.username if self.user else "System"
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {actor} - {self.action}: {self.object_type} #{self.object_id}"
