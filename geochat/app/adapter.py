from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


from .models import *

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super(SocialAccountAdapter, self).save_user(request, sociallogin, form)
        user_add = UserAdditionals()
        user_add.user = user
        user_add.balance = 1000
        #user_add.image = user.socialaccount_set.filter(provider='vk')[0].extra_data['photo']
        user_add.save()
