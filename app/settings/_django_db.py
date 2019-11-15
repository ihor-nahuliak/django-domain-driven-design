import os


DATABASE_HOST = os.environ.get('DATABASE_HOST', '127.0.0.1')
DATABASE_PORT = os.environ.get('DATABASE_PORT', '5432')
DATABASE_USERNAME = os.environ.get('DATABASE_USERNAME', 'postgres')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', '')
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'project')

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT,
        'USER': DATABASE_USERNAME,
        'PASSWORD': DATABASE_PASSWORD,
        'NAME': DATABASE_NAME,
        'TEST': {'NAME': DATABASE_NAME + '_testing'}
    }
}
