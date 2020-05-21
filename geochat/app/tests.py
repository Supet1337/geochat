"""tests.py"""
import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import request
from django.urls import reverse, resolve


# pylint:disable=import-error, unused-argument, wrong-import-order, invalid-name, missing-function-docstring, no-member, undefined-variable, no-self-use, unused-variable, missing-class-docstring

def create_test_user_and_force_login(client, username='Test'):
    user = get_user_model().objects.create_user(username=username, password='Asdfgh12345')
    user.save()
    client.force_login(user=user)
    return client, user


def create_test_user(client, username='Test'):
    user = get_user_model().objects.create_user(username=username, password='Asdfgh12345')
    user.save()
    return user


@pytest.mark.django_db(transaction=True)
class TestIndex:

    def test_visit_index_authorized(self, client):
        client, user = create_test_user_and_force_login(client)
        response = client.get('/')
        assert response.status_code == 301

    def test_visit_index_authorized_check_user(self, client):
        user = create_test_user_and_force_login(client)
        response = client.get('/')
        me = User.objects.get(username='Test')
        request.user = me
        assert response.status_code == 301

    def test_visit_index_authorized_check_username(self, client):
        user = create_test_user_and_force_login(client)
        response = client.get('/')
        me = User.objects.get(username='Test')
        assert me.username == 'Test'
        assert response.status_code == 301

    def test_visit_index_authorized_check_is_not_superuser(self, client):
        user = create_test_user_and_force_login(client)
        response = client.get('/')
        me = User.objects.get(username='Test')
        assert me.is_superuser == 0
        assert response.status_code == 301

    def test_visit_index_authorized_check_is_not_staff(self, client):
        user = create_test_user_and_force_login(client)
        response = client.get('/')
        me = User.objects.get(username='Test')
        assert me.is_staff == 0
        assert response.status_code == 301

    def test_visit_index_authorized_check_is_active(self, client):
        user = create_test_user_and_force_login(client)
        response = client.get('/')
        me = User.objects.get(username='Test')
        assert me.is_active == 1
        assert response.status_code == 301

    def test_visit_index_authorized_check_balance(self, client):
        user = create_test_user_and_force_login(client)
        response = client.get('/')
        me = UserAdditionals.objects.get(user_id=user.id)
        assert me.balance == 1000
        assert response.status_code == 301

    def test_visit_index_authorized_check_balance_update(self, client):
        user = create_test_user_and_force_login(client)
        me = UserAdditionals.objects.get(user_id=user.id)
        old_balance = me.balance
        response = client.get('/ajax-update-balance')
        assert me.balance - old_balance == 1
        assert response.status_code == 301

    def test_visit_index_anonymous(self, client):
        response = client.get('/')
        assert response.status_code == 301


@pytest.mark.django_db(transaction=True)
class TestUrls:

    def test_index_url(self):
        path = reverse('index')
        assert resolve(path).view_name == 'index'

    def test_profile_setting_url(self):
        path = reverse('profile-settings')
        assert resolve(path).view_name == 'profile-settings'

    def test_accounts_signup_url(self):
        path = reverse('accounts/signup')
        assert resolve(path).view_name == 'accounts/signup'

    def test_accounts_login_url(self):
        path = reverse('accounts/login')
        assert resolve(path).view_name == 'accounts/login'

    def test_accounts_logout_url(self):
        path = reverse('accounts/logout')
        assert resolve(path).view_name == 'accounts/logout'

    def test_ajax_update_balancea_url(self):
        path = reverse('ajax-update-balance')
        assert resolve(path).view_name == 'ajax-update-balance'

    def test_ajax_update_circle_draw_url(self):
        path = reverse('ajax-circle-draw')
        assert resolve(path).view_name == 'ajax-circle-draw'

    def test_ajax_update_circle_draw_joined_url(self):
        path = reverse('ajax-circle-draw-joined')
        assert resolve(path).view_name == 'ajax-circle-draw-joined'

    def test_register_user_url(self):
        path = reverse('register-user')
        assert resolve(path).view_name == 'register-user'

    def test_login_user_url(self):
        path = reverse('login-user')
        assert resolve(path).view_name == 'login-user'

    def test_send_report_url(self):
        path = reverse('send-report')
        assert resolve(path).view_name == 'send-report'

    def test_create_room_url(self):
        path = reverse('create-room')
        assert resolve(path).view_name == 'create-room'

    def test_join_room_url(self):
        path = reverse('join-room')
        assert resolve(path).view_name == 'join-room'

    def test_update_profile_settings_url(self):
        path = reverse('update-profile-settings')
        assert resolve(path).view_name == 'update-profile-settings'

    def test_update_profile_picture_url(self):
        path = reverse('update-profile-picture')
        assert resolve(path).view_name == 'update-profile-picture'

    def test_bad_url(self, client):
        response = client.get('/bad_url')
        assert response.status_code == 301

    def test_bad_url_auth(self, client):
        user = create_test_user_and_force_login(client)
        response = client.get('/bad_url')
        assert response.status_code == 301

    def test_ok_url_redirect(self, client):
        response = client.get('/profile/1')
        assert response.status_code == 301

    def test_ok_url_redirect_auth(self, client):
        user = create_test_user_and_force_login(client)
        response = client.get('/profile/1')
        assert response.status_code == 301


@pytest.mark.django_db(transaction=True)
class TestProfileSettings:

    def test_visit_profile_setting_authorized(self, client):
        user = create_test_user_and_force_login(client)
        response = client.get('/profile-settings')
        assert response.status_code == 301


@pytest.mark.django_db(transaction=True)
class TestForms:

    def test_form_profile_settings_status(self, client):
        user = create_test_user_and_force_login(client)
        me = UserAdditionals.objects.get(user_id=user.id)
        response = client.get('/profile-settings')
        assert response.status_code == 301
        user_status_old = me.status
        response = client.get('/profile-settings')
        assert response.status_code == 301
        response = client.get('/update-profile-settings')
        assert response.status_code == 301
        me.status = 'Новый статус'
        assert me.status != user_status_old

    def test_form_profile_settings_private_chats(self, client):
        user = create_test_user_and_force_login(client)
        me = UserAdditionals.objects.get(user_id=user.id)
        response = client.get('/profile-settings')
        assert response.status_code == 301
        user_private_chats_old = me.private_chats
        response = client.get('/profile-settings')
        assert response.status_code == 301
        response = client.get('/update-profile-settings')
        assert response.status_code == 301
        me.private_chats = not user_private_chats_old
        assert me.private_chats != user_private_chats_old

    def test_form_profile_settings_private_info(self, client):
        user = create_test_user_and_force_login(client)
        me = UserAdditionals.objects.get(user_id=user.id)
        response = client.get('/profile-settings')
        assert response.status_code == 301
        user_private_info_old = me.private_info
        response = client.get('/profile-settings')
        assert response.status_code == 301
        response = client.get('/update-profile-settings')
        assert response.status_code == 301
        me.private_chats = not user_private_info_old
        assert me.private_chats != user_private_info_old

    def test_form_profile_settings_user_id(self, client):
        user = create_test_user_and_force_login(client)
        me = UserAdditionals.objects.get(user_id=user.id)
        response = client.get('/profile-settings')
        assert response.status_code == 301
        response = client.get('/profile-settings')
        assert response.status_code == 301
        response = client.get('/update-profile-settings')
        assert response.status_code == 301
        assert user.id == me.user_id

    def test_form_profile_settings_image(self, client):
        user = create_test_user_and_force_login(client)
        me = UserAdditionals.objects.get(user_id=user.id)
        response = client.get('/profile-settings')
        assert response.status_code == 301
        user_image_old = me.image.url
        response = client.get('/profile-settings')
        assert response.status_code == 301
        response = client.get('/update-profile-settings')
        assert response.status_code == 301
        assert me.image.url == user_image_old

    def test_form_profile_settings_image_update(self, client):
        user = create_test_user_and_force_login(client)
        me = UserAdditionals.objects.get(user_id=user.id)
        response = client.get('/profile-settings')
        assert response.status_code == 301
        user_image_old = me.image.url
        response = client.get('/profile-settings')
        assert response.status_code == 301
        response = client.get('/update-profile-picture')
        me.image.url = 'https://medialeaks.ru/wp-content/uploads/2020/02/EPyWlBbWkAEL4du.jpeg'
        assert response.status_code == 301
        assert me.image.url != user_image_old

    def test_form_profile_settings_balance(self, client):
        user = create_test_user_and_force_login(client)
        me = UserAdditionals.objects.get(user_id=user.id)
        response = client.get('/profile-settings')
        assert response.status_code == 301
        user_image_old = me.image.url
        response = client.get('/profile-settings')
        assert response.status_code == 301
        response = client.get('/update-profile-picture')
        me.image.url = 'https://medialeaks.ru/wp-content/uploads/2020/02/EPyWlBbWkAEL4du.jpeg'
        assert response.status_code == 301
        assert me.image.url != user_image_old
