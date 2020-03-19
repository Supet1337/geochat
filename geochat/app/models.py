from django.db import models
from django.contrib.auth.models import User
from django.utils import dateformat
from django.conf import settings
from django.contrib.auth.hashers import make_password
# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=50)
    is_private = models.BooleanField(default=False)

    def save(self, **kwargs):
        self.password = make_password(self.password)
        super().save(**kwargs)

class Message(models.Model):
    text = models.CharField(max_length=250)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)

    def json(self):
        datef = dateformat.format(self.date,settings.DATE_FORMAT)
        return  {'text':self.text, 'author': str(self.author), 'date':str(datef)}


