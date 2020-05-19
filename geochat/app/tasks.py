from celery import shared_task
from django.http import request
from django.contrib import messages
from .models import *
import redis

@shared_task
def geocoin_daily_bonus():
    red = redis.Redis(host='redis', port=6379) #TODO исправить на 6379
    for user in User.objects.all():
        if user.is_authenticated:
            red_name = user.username
            red.set(red_name, 200)
    red.close()
