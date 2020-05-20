"""urls.py"""
# pylint:disable=wildcard-import, unused-wildcard-import
from django.urls import path
from .views import *

urlpatterns = [
    path('room/<int:number>', room),
    path('accounts/login', redirect_login),
    path('accounts/signup', redirect_signup),
    path('', index, name='index'),
    path('logout', loggout),
    path('ajax-update-balance', ajax_update_balance),
    path('ajax-maps-draw/<int:number>', ajax_maps_draw),
    path('ajax-circle-draw', ajax_circle_draw),
    path('ajax-circle-draw-joined', ajax_circle_draw_joined),
    path('ajax-load-messages/<int:number>', ajax_load_messages),
    path('profile/<int:number>', profile),
    path('profile-settings', profile_settings, name='profile-settings'),
    path('delete-room/<int:number>', delete_room),
    path('register-user', register_user),
    path('login-user', login_user),
    path('send-report', report),
    path('create-room', create_room),
    path('join-room', join_room),
    path('update-profile-settings', update_profile_settings),
    path('update-profile-picture', update_profile_picture),
    path('update-room-picture/<int:number>', update_room_picture),
    path('update-room-settings/<int:number>', update_room_settings),
    path('leave-chat/<int:number>', leave_chat),
    path('doc', doc),

]
