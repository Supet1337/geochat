from django.db import models
from django.contrib.auth.models import User
from django.utils import dateformat
from django.conf import settings
# Create your models here.

class Message(models.Model):
    text = models.CharField(max_length=250)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def json(self):
        datef = dateformat.format(self.date,settings.DATE_FORMAT)
        return  {'text':self.text, 'author': str(self.author), 'date':str(datef)}

class Circle(models.Model):
    x = models.FloatField()
    y = models.FloatField()

    def json(self):
        return  {'x':self.x, 'y':self.y}
