from .views import *
from django.urls import path

urlpatterns = [
    path('rooms',rooms),
    path('create-room',create_room),
    path('room/<int:number>', room),
    path('',index),
    path('ajax/<int:number>',ajax_send),
    path('ajax-update/<int:number>',ajax_update),
]
