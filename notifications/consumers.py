import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.conf import settings

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
            return

        # Join user's personal notification group
        self.user_id = str(self.scope["user"].id)
        self.group_name = f"user_{self.user_id}"
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')
        
        # Echo the message back to the user
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'notification',
                'message': message
            }
        )

    async def notification(self, event):
        # Send notification to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'notification_type': event.get('notification_type', '')
        })) 