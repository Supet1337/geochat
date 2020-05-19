import os
from celery import Celery
from celery import task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geochat.settings')

app = Celery('geochat')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
