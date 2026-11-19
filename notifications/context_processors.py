def unread_notifications_processor(request):
    """Provides unread notifications count globally to templates."""
    if request.user.is_authenticated:
        try:
            from .models import Notification
            count = Notification.objects.filter(recipient=request.user, is_read=False).count()
            recent = Notification.objects.filter(recipient=request.user)[:5]
            return {
                "unread_notifications_count": count,
                "header_notifications": recent
            }
        except Exception:
            return {"unread_notifications_count": 0, "header_notifications": []}
    return {"unread_notifications_count": 0, "header_notifications": []}
