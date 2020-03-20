from .views import *
from django.urls import path

urlpatterns = [
    path('chat', chat),
    path('',index),
    path('ajax_circle',ajax_circle),
    path('ajax-circle-draw',ajax_circle_draw),
    path('ajax',ajax_send),
    path('ajax-update',ajax_update),
    path('chad',chad),
]
