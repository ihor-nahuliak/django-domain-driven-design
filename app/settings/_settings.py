import os


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', None)

DEBUG = os.environ.get('DJANGO_DEBUG', False)

PROJECT_ROOT = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

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
if DEBUG:
    REQUIREMENTS_APPS.append('debug_toolbar')

PROJECT_APPS = [
]

INSTALLED_APPS = REQUIREMENTS_APPS + PROJECT_APPS

REQUIREMENTS_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
if DEBUG:
    REQUIREMENTS_MIDDLEWARE.append(
        'debug_toolbar.middleware.DebugToolbarMiddleware'
    )

PROJECT_MIDDLEWARE = [
]

MIDDLEWARE = REQUIREMENTS_MIDDLEWARE + PROJECT_MIDDLEWARE

DATABASE_HOST = os.environ.get('DATABASE_HOST', '127.0.0.1')
DATABASE_PORT = os.environ.get('DATABASE_PORT', '5432')
DATABASE_USERNAME = os.environ.get('DATABASE_USERNAME', 'postgres')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', '')
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'project')

if not DATABASE_NAME.endswith('_testing'):
    TESTING_DATABASE_NAME = DATABASE_NAME + '_testing'
else:
    TESTING_DATABASE_NAME = DATABASE_NAME

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT,
        'USER': DATABASE_USERNAME,
        'PASSWORD': DATABASE_PASSWORD,
        'NAME': DATABASE_NAME,
        'TEST': {'NAME': TESTING_DATABASE_NAME}
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.NumericPasswordValidator',
    },
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
