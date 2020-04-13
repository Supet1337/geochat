from django.contrib import admin
from .models import Wallet, Room, Message, JoinRoom, Image

admin.site.register(Wallet)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(JoinRoom)
admin.site.register(Image)
# Register your models here.
