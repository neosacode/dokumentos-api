import os

import dj_database_url
from prettyconf import Configuration
from dokumentos_api.casts import redis_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = Configuration(starting_path=BASE_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=config.boolean)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=config.list)


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    'apps.core',
    'apps.documents',
    'apps.webhook',
    'apps.ocr',
]

THIRD_PARTY_APPS = [
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'dokumentos_api.urls'

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


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'PAGINATE_BY': 10
}

WSGI_APPLICATION = 'dokumentos_api.wsgi.application'

# Security options
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=True, cast=config.boolean)
SECURE_CONTENT_TYPE_NOSNIFF = config('SECURE_CONTENT_TYPE_NOSNIFF', default=True, cast=config.boolean)
SECURE_BROWSER_XSS_FILTER = config('SECURE_BROWSER_XSS_FILTER', default=True, cast=config.boolean)
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=config.boolean)
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=True, cast=config.boolean)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=config.boolean)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=config.boolean)
SESSION_COOKIE_HTTPONLY = config('SESSION_COOKIE_HTTPONLY', default=True, cast=config.boolean)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=config.boolean)
CSRF_COOKIE_HTTPONLY = config('CSRF_COOKIE_HTTPONLY', default=True, cast=config.boolean)
X_FRAME_OPTIONS = config('X_FRAME_OPTIONS', default='DENY')


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {}
DATABASES['default'] = dj_database_url.parse(config('DATABASE_URL'))


# S3 Bucket
S3_BUCKET = config('S3_BUCKET')

# Webhook engine

WEBHOOK_MAXIMUM_STACK_SIZE = config('WEBHOOK_MAXIMUM_STACK_SIZE', default=30, cast=int)
WEBHOOK_MAXIMUM_TRIES = config('WEBHOOK_MAXIMUM_TRIES', default=5, cast=int)
WEBHOOK_QUEUE_NAME = config('WEBHOOK_QUEUE_NAME')

# OCR engine

OCR_GOOGLECLOUD_KEY = config('OCR_GOOGLECLOUD_KEY')

# Redis session config
SESSION_REDIS = config('REDIS_URL', default=None, cast=redis_url)

if SESSION_REDIS:
    SESSION_ENGINE = 'redis_sessions.session'


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# Overwrite defaul user model
AUTH_USER_MODEL = 'core.User'

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
