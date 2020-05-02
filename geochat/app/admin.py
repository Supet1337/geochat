from django.contrib import admin
from .models import Room, Message, JoinRoom, UserAdditionals

admin.site.register(UserAdditionals)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(JoinRoom)
# Register your models here.
