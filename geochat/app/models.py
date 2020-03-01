from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Message(models.Model):
    text = models.CharField(max_length=250)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def json(self):
        return  {'text':self.text, 'author': str(self.author), 'date':str(self.date)}


