"""models.py"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import dateformat
from django.conf import settings
from django.contrib.auth.hashers import make_password


# pylint:disable=too-many-instance-attributes

def user_directory_path(instance, filename):
    """
    Функция возврата пути изображения для профиля

    :param instance: Пример
    :param filename: Имя файла
    :return: Возвращает путь к файлу
    """
    return 'avatars/user_{0}/{1}'.format(instance.user.id, filename)


def room_directory_path(instance, filename):
    """
    Функция возврата пути изображения для комнаты

    :param instance: Пример
    :param filename: Имя файла
    :return: Возвращает путь к файлу
    """
    return 'room_images/room_{0}/{1}'.format(instance.id, filename)


class Room(models.Model):
    """
    Модель для хранения чатов.
    """

    name = models.CharField(max_length=50)
    """Название комнаты"""
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    """Автор комнаты"""
    date = models.DateTimeField(auto_now_add=True)
    """Дата создания комнаты"""
    password = models.CharField(max_length=50)
    """Пароль комнаты"""
    is_private = models.BooleanField(default=False)
    """Параметр приватности комнаты"""
    is_place = models.BooleanField(default=False)
    """Параметр отображения комнаты (If True, Комната будет видна тем, кто находится поблизости)"""
    max_members = models.IntegerField(default=10)
    """Максимальное количество пользователей комнаты"""
    image = models.ImageField(upload_to=room_directory_path, blank=True)
    """Аватар комнаты"""
    x = models.FloatField()
    """Координата Х комнаты"""
    y = models.FloatField()
    """Координата У комнаты"""
    diametr = models.IntegerField(default=300)
    """Диматер комнаты"""

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, **kwargs, ):
        """
        Функция сохранения пароля комнаты (если is_private==True)

        :param kwargs:
        :param force_insert: False
        :param force_update: False
        :param update_fields: None
        :param using: None
        :return: None
        """
        self.password = make_password(self.password)
        super().save(**kwargs)

    def json(self):
        """
        Функция передачи комнат через AJAX.

        :return: x, y, name, author, is_private, is_place, id, diametr, image, members, max_members,
        """
        return {
            'x': self.x,
            'y': self.y,
            'name': self.name,
            'author': str(
                self.author),
            'is_private': self.is_private,
            'is_place': self.is_place,
            'id': str(
                self.id),
            'diametr': self.diametr,
            'image': self.get_image(),
            'members': str(self.members()),
            'max_members': str(self.max_members)}

    def get_image(self):
        """
        Функция получения изображения для чата.

        :return: image.url(если у чата есть аватар), иначе geocoin.png(default)
        """
        try:
            return str(self.image.url)
        except BaseException:  # pylint:disable=bare-except, broad-except
            return 'https://s3.nl-ams.scw.cloud/geochat-static/images/geocoin.png'

    def members(self):
        """
        Функция получения количества пользователей, которые вошли в чат.

        :return: len()
        """
        return len(JoinRoom.objects.filter(room_id=self.id))


class Message(models.Model):
    """
    Модель для хранения сообщений.
    """
    text = models.CharField(max_length=250)
    """Текст сообщения"""
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    """Автор сообщения"""
    date = models.DateTimeField(auto_now_add=True)
    """Дата сообщения"""
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    """Комната, куда отправляется сообщение"""

    def json(self):
        """
        Функция передачи данных сообщения через AJAX.

        :return: text, author, date, image, id
        """
        datef = dateformat.format(self.date, settings.DATE_FORMAT)
        return {
            'text': self.text,
            'author': str(
                self.author),
            'date': str(datef),
            'id': self.author.id,
            'image': str(
                self.get_image())}

    def get_image(self):
        """
        Функция получения изображения для пользователя.

        :return: image.url(если у пользователя есть аватар), иначе -1(default_ava.png)
        """
        try:
            return UserAdditionals.objects.get(user=self.author).image.url
        except BaseException: # pylint:disable=broad-except
            return -1


class JoinRoom(models.Model):
    """
    Модель для хранения чатов, в которые вступил пользователь.
    """

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    """Пользователь"""
    room_id = models.IntegerField()
    """Id комнаты"""
    date = models.DateTimeField(auto_now_add=True)
    """Дата"""


class UserAdditionals(models.Model):
    """
    Модель для дополнительных настроек пользователя.
    """

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    """Пользователь"""
    image = models.ImageField(upload_to=user_directory_path, blank=True)
    """Аватар пользователя"""
    balance = models.IntegerField(default=1000)
    """Баланс пользователя (geocoin)"""
    status = models.CharField(max_length=50, default='Статус не указан')
    """Статус пользователя"""
    private_chats = models.BooleanField(default=False)
    """Параметр приватности (Не будут показываться чаты другим пользователям)"""
    private_info = models.BooleanField(default=False)
    """Параметр приватности (Не будут показываться статус и баланс другим пользователям)"""


class Report(models.Model):
    """
    Модель для хранения Репортов.
    """

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    """Пользователь"""
    report = models.CharField(max_length=250)
    """Сообщение репорта"""
    date = models.DateTimeField(auto_now_add=True)
    """Дата отправки репорта"""
