from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(recipient=request.user)
    return render(request, "notifications/list.html", {"notifications": notifications})


@login_required
def notification_mark_read(request, notification_id):
    notif = get_object_or_404(Notification, pk=notification_id, recipient=request.user)
    notif.is_read = True
    notif.save(update_fields=["is_read"])
    if notif.link_url:
        return redirect(notif.link_url)
    return redirect("notification_list")


@login_required
def notification_mark_all_read(request):
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return redirect("notification_list")


@login_required
def api_unread_notifications(request):
    """API endpoint providing live unread count and latest messages."""
    qs = Notification.objects.filter(recipient=request.user)
    unread_count = qs.filter(is_read=False).count()
    recent = qs[:5]
    items = []
    for n in recent:
        items.append({
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "notification_type": n.notification_type,
            "link_url": n.link_url,
            "is_read": n.is_read,
            "created_at": n.created_at.strftime("%d-%b %H:%M")
        })
    return JsonResponse({"unread_count": unread_count, "items": items})
