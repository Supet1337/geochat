"""Consumers.py"""
import json
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import User, UserAdditionals, Room, Message  # pylint: disable=wildcard-import



# pylint: disable=no-self-use, no-else-return, attribute-defined-outside-init

class ChatConsumer(AsyncWebsocketConsumer):
    """
    Консумер чата.
    """

    async def connect(self):
        """
        Функция подключения к вебсокету чата.

        :return: None
        """
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_id

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        """
        Функция отключения от вебсокета чата.

        :param code: Код дисконекта
        :return: None
        """
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Получение сообщения клиента, Сохранение в БД, Отправка на сервер

    async def receive(self, text_data=None, bytes_data=None):
        """
        Функция получения информации и сохранения её в базу данных.

        :param text_data: информация сообщения
        :param bytes_data: информация сообщения
        :return: None
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        author_id = text_data_json['author_id']
        room = text_data_json['room_id']
        await database_sync_to_async(self.save_message)(message, author_id, room)
        author_name = await database_sync_to_async(self.get_name)(author_id)
        author_image = await database_sync_to_async(self.get_image)(author_id)
        now = datetime.now()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'id': author_id,
                'author_name': author_name,
                'author_image': author_image,
                'date': now.strftime("%d.%m %H:%M")
            }
        )

    # Сохранение сообщений в БД
    def save_message(self, message, author, room):
        """
        Функция сохранения сообщений в базу данных.

        :param message: сообщение
        :param author: автор
        :param room: комната
        :return: None
        """
        new_message = Message()
        new_message.author = User.objects.get(id=author)
        new_message.room = Room.objects.get(id=room)
        new_message.text = message
        new_message.save()

    # Получить имя
    def get_name(self, author):
        """
        Функция получения имени пользователя.

        :param author: автор
        :return: username
        """
        return User.objects.get(id=author).username

    def get_image(self, user):
        """
         Функция получения изображения пользователя.

        :param user: user
        :return: image.url(если у пользователя есть аватар), иначе -1
        """
        user_add = UserAdditionals.objects.get(user_id=user)
        if user_add.image == '':
            return '-1'
        else:
            return user_add.image.url

    async def chat_message(self, event):
        """
        Функция отправки сообщений Вебсокету.

        :param event: событие
        :return: None
        """
        message = event['message']
        author_name = event['author_name']
        author_image = event['author_image']
        author_id = event['id']
        date = event['date']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'id': author_id,
            'author_name': author_name,
            'author_image': author_image,
            'date': date
        }))
