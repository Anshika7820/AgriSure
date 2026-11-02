import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.room_group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            "type": "notification",
            "title": event["title"],
            "message": event["message"],
            "notification_type": event.get("notification_type", "SYSTEM"),
            "link_url": event.get("link_url", ""),
            "created_at": event.get("created_at", "")
        }))


class NegotiationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.offer_id = self.scope["url_route"]["kwargs"]["offer_id"]
        self.room_group_name = f"negotiation_{self.offer_id}"

        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "")
        counter_price = data.get("counter_price")
        counter_qty = data.get("counter_qty")

        # Broadcast to room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "negotiation_message",
                "sender_id": self.user.id,
                "sender_name": self.user.get_full_name() or self.user.username,
                "message": message,
                "counter_price": counter_price,
                "counter_qty": counter_qty,
            }
        )

    async def negotiation_message(self, event):
        await self.send(text_data=json.dumps(event))
