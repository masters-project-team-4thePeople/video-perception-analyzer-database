import os
import logging
import dj_database_url
import yaml
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# read config file
with open("config.yaml", "r") as stream:
    try:
        config_file = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        logging.error(exc)

print(config_file)

# extract keys using decouple module
SECRET_KEY = config_file["SECRET_KEY"]
DEBUG = config_file["DEBUG"]
ALLOWED_HOSTS = config_file["ALLOWED_HOSTS"]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # django rest framework app
    'drf_yasg',  # documentation app
    'storages',  # storages app
    'users_api',  # users app
    'videos_api',  # videos app
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

ROOT_URLCONF = 'database_microservice.urls'
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

WSGI_APPLICATION = 'database_microservice.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
if DEBUG:
    print("Using Local Postgresql Database")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'USER': 'postgres',
            'NAME': 'masters_project_database',  # add your local username here
            'PASSWORD': 'dummypassword',  # add your local db password here
            'HOST': 'localhost',
            'PORT': '5432'
        }
    }
else:
    print("Using Digital Ocean Postgresql Database")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config_file['postgres_database']['database'],
            'USER': config_file['postgres_database']['username'],
            'PASSWORD': config_file['postgres_database']['password'],
            'HOST': config_file['postgres_database']['host'],
            'PORT': config_file['postgres_database']['port']
        }
    }
    # database connection check in seconds
    db_from_env = dj_database_url.config(conn_max_age=1000)
    DATABASES['default'].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
# Static and media files settings
USE_SPACES = config_file["digital_ocean"]['USE_SPACES']

print(USE_SPACES)

if USE_SPACES:
    AWS_ACCESS_KEY_ID = config_file["digital_ocean"]["access_key"]
    AWS_SECRET_ACCESS_KEY = config_file["digital_ocean"]["secret_key"]
    AWS_STORAGE_BUCKET_NAME = config_file["digital_ocean"]["bucket_name"]

    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_ENDPOINT_URL = config_file["digital_ocean"]["endpoint_url"]
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

    # static settings
    AWS_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    # public media settings
    PUBLIC_MEDIA_LOCATION = 'media/users/'
    MEDIA_URL = f'https://{AWS_S3_ENDPOINT_URL}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'database_microservice.storage_backends.PublicMediaStorage'
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'mediafiles'


STATICFILES_DIRS = (BASE_DIR / 'static',)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users_api.UserProfile'
