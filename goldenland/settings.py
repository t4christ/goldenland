"""
Django settings for goldenland project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+3)gbxi(+qrj8^s8@%zu%3p@bq&vs64mkv14*&kl&&2a8but6c'

#Environment variables
import dotenv
from dotenv import load_dotenv
dotenv.load_dotenv()
load_dotenv(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gunicorn',
    'cloudinary_storage',
    'cloudinary',
    # 'djangocloudistatic',
    'crispy_forms',
    'gdapp'
]



CRISPY_TEMPLATE_PACK = "bootstrap4"

AUTH_USER_MODEL = 'gdapp.MyUser'

CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")

CLOUDI_NAME = os.getenv('CLOUDINARY_NAME')
CLOUDI_API_KEY = os.getenv('CLOUDINARY_API_KEY')
CLOUDI_API_SECRET = os.getenv('CLOUDINARY_SECRET_KEY')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'goldenland.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'goldenland.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if DEBUG:
    DATABASES = {
        # 'default': {
        #     'ENGINE': 'django.db.backends.sqlite3',
        #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # }
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv("POSTGRES_DBNAME"),
            'USER' : os.getenv("POSTGRES_USER"),
            'PASSWORD': os.getenv("POSTGRES_PASS"),
            'PORT': '5432',
            'HOST':os.getenv("POSTGRES_HOST"),
        },
        'realtor': {
            'ENGINE': 'djongo',
            'NAME': os.getenv("MONGO_DBNAME"),
            'ENFORCE_SCHEMA': False,
            # 'CLIENT': {
            #     'host': 'mongodb+srv://<username>:<password>@<atlas cluster>/<myFirstDatabase>?retryWrites=true&w=majority'
            # } 
        }

    }
else:
    DATABASES = {
      'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("NAME"),
        'USER' : os.getenv("USER"),
        'PASSWORD': os.getenv("PASSWORD"),
        'PORT': '5432',
        'HOST':os.getenv("HOST"),
    },
            'realtor': {
            'ENGINE': 'djongo',
            'NAME': os.getenv("MONGO_DBNAME"),
            'ENFORCE_SCHEMA': False,
            # 'CLIENT': {
            #     'host': 'mongodb+srv://<username>:<password>@<atlas cluster>/<myFirstDatabase>?retryWrites=true&w=majority'
            # } 
        }
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

# USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
if DEBUG:
    STATIC_URL = '/static/'
    STATIC_ROOT = 'staticfiles'
    STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    )
    MEDIA_URL = '/media/'
    MEDIA_ROOT=os.path.join(BASE_DIR,'media')
else:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    STATIC_ROOT = 'staticfiles'
    STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    )
    # STATIC_URL = 'https://res.cloudinary.com/glodenlanders/raw/upload/v1/static/'
    STATIC_URL = '/static/'
    STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'

CLOUDINARY_STORAGE = {
    # other settings, like credentials
    'MEDIA_TAG': 'media',
    'STATIC_TAG': 'static',
    'MAGIC_FILE_PATH': 'magic',
    'PREFIX': '/media/',
    'STATICFILES_MANIFEST_ROOT': os.path.join(BASE_DIR, 'manifest')
}

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#              'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
#         },
#     },
# }