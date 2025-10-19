import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Room, Message

User = get_user_model()
logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        logger.info(f"WebSocket connected to room: {self.room_name}")
        logger.info(f"User: {self.scope['user']}")

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # logger.info(f"Received data: {text_data}")
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        # logger.info(f"Message: {message}, Username: {username}")

        try:
            await self.save_message(username, self.room_name, message)
            logger.info("Message saved successfully")
        except Exception as e:
            logger.info(f"Error saving message: {e}")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    async def chat_message(self, event):
        logger.info(f"Broadcasting message: {event}")
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username']
        }))

    @database_sync_to_async
    def save_message(self, username, room_name, message):
        # logger.info(f"Attempting to save - User: {username}, Room: {room_name}, Message: {message}")
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room_name)
        msg = Message.objects.create(user=user, room=room, content=message)
        # logger.info(f"Message created with ID: {msg.id}")
        return msg
