import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *
from datetime import datetime
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_id

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        author_id = text_data_json['author_id']
        room = text_data_json['room_id']
        await database_sync_to_async(self.save_message)(message,author_id,room)
        author_name = await database_sync_to_async(self.get_name)(author_id)
        now = datetime.now()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'author_name': author_name,
                'date': now.strftime("%d.%m %H:%M")
            }
        )

    def save_message(self,message,author,room):
        new_message = Message()
        new_message.author = User.objects.get(id=author)
        new_message.room = Room.objects.get(id=room)
        new_message.text = message
        new_message.save()

    def get_name(self,author):
        return User.objects.get(id=author).username
    async def chat_message(self, event):
        message = event['message']
        author_name = event['author_name']
        date = event['date']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'author_name': author_name,
            'date': date
        }))