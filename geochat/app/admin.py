from django.contrib import admin
from .models import Wallet, Room, Message, JoinRoom

admin.site.register(Wallet)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(JoinRoom)
# Register your models here.
