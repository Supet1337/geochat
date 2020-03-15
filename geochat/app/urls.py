from .views import *
from django.urls import path

urlpatterns = [
    path('chat', chat),
    path('',index),
    path('map',map),
]
