import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Room, Message, Conversation, DirectMessage

User = get_user_model()
logger = logging.getLogger(__name__)


# group message consumers
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


# NEW: DM Consumer
class DMConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'dm_{self.conversation_id}'
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

        # Verify user is part of this conversation
        is_participant = await self.check_participant()
        if not is_participant:
            await self.close()
            return

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
        data = json.loads(text_data)
        message = data['message']

        # Save the DM
        saved_message = await self.save_dm(message)

        # Broadcast to conversation participants
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'dm_message',
                'message': message,
                'sender': self.user.username,
                'timestamp': saved_message['timestamp'],
                'message_id': saved_message['id']
            }
        )

    async def dm_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp'],
            'message_id': event['message_id']
        }))

    @database_sync_to_async
    def check_participant(self):
        try:
            conversation = Conversation.objects.get(id=self.conversation_id)
            return conversation.participants.filter(id=self.user.id).exists()
        except Conversation.DoesNotExist:
            return False

    @database_sync_to_async
    def save_dm(self, message):
        conversation = Conversation.objects.get(id=self.conversation_id)
        dm = DirectMessage.objects.create(
            conversation=conversation,
            sender=self.user,
            content=message
        )
        # Update conversation timestamp
        conversation.save()
        return {
            'id': dm.id,
            'timestamp': dm.timestamp.isoformat()
        }
