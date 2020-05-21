"""
Django settings for geochat project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys
from celery.schedules import crontab

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wnt)319w#i$1ug2x)v2q0i_ilx7bia=hk&*1b@j4i%g+fmazfr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
# DEBUG = os.environ.get('DEBUG')

ALLOWED_HOSTS = ['*']

TEST_MODE = 'pytest' in sys.modules
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup.apps.CleanupConfig',
    'channels',
    'app',
    'storages',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.vk',
    'allauth.socialaccount.providers.discord',
]

SITE_ID = 2

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'geochat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['app/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]

WSGI_APPLICATION = 'geochat.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
ASGI_APPLICATION = 'geochat.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis', 6379)],
        },
    },
}
REDIS = {
    'second': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis_coin', 6379)],
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

DATE_FORMAT = 'd.m G:i'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = "./collectedstatic"
MEDIA_ROOT = "./media/"
SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_ADAPTER = 'app.adapter.SocialAccountAdapter'
SOCIALACCOUNT_PROVIDERS = {
    'vk': {
        'SCOPE': ['email']
    }
}

SECURE_SSL_REDIRECT = True
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/'
LOGOUT_REDIRECT_URL = '/'
# s3 serve static

CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_BEAT_SCHEDULE = {
    'update_geocoin_cache': {
        'task': 'app.tasks.geocoin_daily_bonus',
        'schedule': crontab(minute='*/1440')
    }
}

AWS_ACCESS_KEY_ID = "SCWWC0NA79VBS7DQ1G0R"
AWS_SECRET_ACCESS_KEY = "91d10a80-a8c2-49f0-ad3e-62fdad004c9d"
AWS_STORAGE_BUCKET_NAME = "geochat-static"
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_REGION_NAME = "nl-ams"
AWS_S3_ENDPOINT_URL = "https://s3.nl-ams.scw.cloud"

if not DEBUG:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

if DEBUG:
    # `debug` is only True in templates if the vistor IP is in INTERNAL_IPS.
    INTERNAL_IPS = type(str('c'), (), {'__contains__': lambda *a: True})()

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
ACCOUNT_EMAIL_VERIFICATION = "none"
EMAIL_HOST_USER = 'shp.geochat@yandex.ru'
EMAIL_HOST_PASSWORD = 'srgobbbgbhzoeias'
DEFAULT_FROM_EMAIL = 'shp.geochat@yandex.ru'

FIXTURE_DIRS = ['app/fixtures', 'geochat/app/fixtures', 'geochat/geochat/app/fixtures', './geochat/geochat/app/fixtures', '.././app/fixtures']
