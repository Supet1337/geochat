"""tasks.py"""
# pylint:disable=unused-wildcard-import, wildcard-import, wrong-import-order
from celery import shared_task
from .models import *
import redis

@shared_task
def geocoin_daily_bonus():
    """
    Таск по выдачи ежедневного бонуса геокоинов.
    """
    red = redis.Redis(host='redis', port=6379)
    for user in User.objects.all():
        if user.is_authenticated:
            red_name = user.username
            red.set(red_name, 200)
    red.close()
