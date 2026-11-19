from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/notifications/$", consumers.NotificationConsumer.as_asgi()),
    re_path(r"ws/negotiations/(?P<offer_id>\d+)/$", consumers.NegotiationConsumer.as_asgi()),
]
