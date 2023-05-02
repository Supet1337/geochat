"""forms.py"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserAdditionals, Room

class UserSettingsForm(forms.ModelForm):
    """
    Форма загрузки изображения для пользователя.
    """

    class Meta:
        model = UserAdditionals
        fields = ['image']


class RoomSettingsForm(forms.ModelForm):
    """
    Форма загрузки изображения для чата.
    """

    class Meta:
        model = Room
        fields = ['image']


class RegisterForm(UserCreationForm):
    """
    Форма регистрации пользователя.
    """
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):  # pylint:disable=useless-super-delegation
        super(RegisterForm, self).__init__(*args, **kwargs)
        # do not require password confirmation
