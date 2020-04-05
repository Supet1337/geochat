from .views import *
from django.urls import path

urlpatterns = [
    path('room/<int:number>', room),
    path('',index),
    path('ajax-update-balance',ajax_update_balance),
    path('ajax-maps-draw/<int:number>',ajax_maps_draw),
    path('ajax-circle-draw',ajax_circle_draw),
    path('ajax-circle-draw-joined',ajax_circle_draw_joined),
    path('ajax-load-messages/<int:number>',ajax_load_messages),
    path('profile/<int:number>',profile),
]
