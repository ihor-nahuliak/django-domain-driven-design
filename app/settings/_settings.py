import os


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', None)

DEBUG = os.environ.get('DJANGO_DEBUG', False)

PROJECT_ROOT = os.path.abspath(
    os.path.join(__file__, os.pardir, os.pardir, os.pardir))

WSGI_APPLICATION = 'wsgi.application'

ROOT_URLCONF = 'urls'

STATIC_URL = '/static/'

USE_X_FORWARDED_HOST = True  # Make ViewSet paginate with origin host url

# TODO: Allow just the ones that are being used
ALLOWED_HOSTS = ['*']

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

REQUIREMENTS_APPS = [
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

PROJECT_APPS = [
]

REQUIREMENTS_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

PROJECT_MIDDLEWARE = [
]
