"""urls.py"""
# pylint:disable=wildcard-import, unused-wildcard-import
from django.urls import path
from .views import *

urlpatterns = [
    path('room/<int:number>', room),
    path('accounts/login', redirect_login,  name='accounts/login'),
    path('accounts/signup', redirect_signup,  name='accounts/signup'),
    path('', index, name='index'),
    path('logout', loggout, name='logout'),
    path('ajax-update-balance', ajax_update_balance, name='ajax-update-balance'),
    path('ajax-maps-draw/<int:number>', ajax_maps_draw),
    path('ajax-circle-draw', ajax_circle_draw, name='ajax-circle-draw'),
    path('ajax-circle-draw-joined', ajax_circle_draw_joined, name='ajax-circle-draw-joined'),
    path('ajax-load-messages/<int:number>', ajax_load_messages),
    path('profile/<int:number>', profile),
    path('profile-settings', profile_settings, name='profile-settings'),
    path('delete-room/<int:number>', delete_room),
    path('register-user', register_user, name='register-user'),
    path('login-user', login_user, name='login-user'),
    path('send-report', report, name='send-report'),
    path('create-room', create_room,  name='create-room'),
    path('join-room', join_room, name='join-room'),
    path('update-profile-settings', update_profile_settings, name='update-profile-settings'),
    path('update-profile-picture', update_profile_picture, name='update-profile-picture'),
    path('update-room-picture/<int:number>', update_room_picture),
    path('update-room-settings/<int:number>', update_room_settings),
    path('leave-chat/<int:number>', leave_chat),
    path('doc', doc),

]
