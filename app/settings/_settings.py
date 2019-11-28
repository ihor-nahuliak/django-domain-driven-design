import os
import typing

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'testing')

DEBUG = bool(os.getenv('DJANGO_DEBUG'))

PROJECT_ROOT = os.path.abspath(
    os.path.join(__file__, os.pardir, os.pardir, os.pardir)
)

WSGI_APPLICATION = 'wsgi.application'

ROOT_URLCONF = 'urls'

STATIC_URL = '/static/'

USE_X_FORWARDED_HOST = True  # Make ViewSet paginate with origin host url

ALLOWED_HOSTS = ['*']

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

REQUIREMENTS_APPS: typing.List[str] = [
    # django:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    # django-oauth-toolkit:
    'oauth2_provider',
    # djangorestframework:
    'rest_framework',
    'rest_framework.authtoken',
    # django-modeltranslation:
    'modeltranslation',
    # django-admin:
    'django.contrib.admin',
]

PROJECT_APPS: typing.List[str] = [
]

REQUIREMENTS_MIDDLEWARE: typing.List[str] = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

PROJECT_MIDDLEWARE: typing.List[str] = [
]
