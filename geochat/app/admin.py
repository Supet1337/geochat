from django.contrib import admin
from .models import Room, Message, JoinRoom, UserAdditionals, Report

admin.site.register(UserAdditionals)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(JoinRoom)
admin.site.register(Report)
# Register your models here.
