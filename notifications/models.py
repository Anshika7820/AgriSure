from django.db import models
from django.conf import settings

class Notification(models.Model):
    class NotificationType(models.TextChoices):
        OFFER = "OFFER", "New Offer"
        COUNTER = "COUNTER", "Counter-Offer"
        CONTRACT = "CONTRACT", "Contract Event"
        DELIVERY = "DELIVERY", "Delivery Update"
        PAYMENT = "PAYMENT", "Payment Processed"
        DISPUTE = "DISPUTE", "Dispute Alert"
        SYSTEM = "SYSTEM", "Platform Announcement"

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.SYSTEM
    )
    link_url = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.recipient.username} - {self.title} ({'Read' if self.is_read else 'Unread'})"
