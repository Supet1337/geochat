from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UploadImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['image']

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # do not require password confirmation
