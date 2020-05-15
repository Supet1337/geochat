import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import request
from django.urls import reverse, resolve
#TODO Разобраться нашей бд в pytest

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

    def test_index_url(self):
        path = reverse('index')
        assert resolve(path).view_name == 'index'

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

    def test_visit_index_anonymous(self, client):
        response = client.get('/')
        assert response.status_code == 301

@pytest.mark.django_db(transaction=True)
class TestProfile:

    def test_visit_profile_authorized(self, client):
        user = create_test_user_and_force_login(client)
        response = client.get('/profile/1')
        assert response.status_code == 301

@pytest.mark.django_db(transaction=True)
class TestProfileSettings:

    def test_profile_setting_url(self):
        path = reverse('profile-settings')
        assert resolve(path).view_name == 'profile-settings'

    def test_visit_profile_setting_authorized(self, client):
        user = create_test_user_and_force_login(client)
        response = client.get('/profile-settings')
        assert response.status_code == 301