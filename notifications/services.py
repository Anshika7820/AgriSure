from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

def send_user_notification(user, title, message, notification_type="SYSTEM", link_url=""):
    """
    Creates persistent notification in database and broadcasts over WebSockets
    to connected user session if available.
    """
    notif = Notification.objects.create(
        recipient=user,
        title=title,
        message=message,
        notification_type=notification_type,
        link_url=link_url
    )

    try:
        channel_layer = get_channel_layer()
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                f"user_{user.id}",
                {
                    "type": "send_notification",
                    "title": title,
                    "message": message,
                    "notification_type": notification_type,
                    "link_url": link_url,
                    "created_at": notif.created_at.strftime("%H:%M")
                }
            )
    except Exception as e:
        # Fallback gracefully if channel layer is offline or during testing
        pass

    return notif
