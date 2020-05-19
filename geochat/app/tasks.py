from celery import shared_task
from .models import *
import redis

@shared_task
def geocoin_daily_bonus():
    for user in User.objects.all():
        user_add = UserAdditionals.objects.get(user=user)
        if user_add is not None:
            user_add.balance += 100
        user_add.save()
        pass
