from .views import *
from django.urls import path

urlpatterns = [
    path('chat', chat),
    path('',index),
    path('ajax',ajax_send),
    path('ajax-update',ajax_update),
    path('map',map),
]
