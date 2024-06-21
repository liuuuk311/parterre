import os
from pathlib import Path
import environ
from django.utils.translation import gettext_lazy as _

env = environ.Env(DEBUG=(bool, False))
env.NOTSET = ""

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(BASE_DIR.parent / ".env")

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env('DJANGO_SECRET_KEY')

DEBUG = env('DEBUG')


INSTALLED_APPS = [
    'csvexport',
    "users.apps.UserConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    'storages',
    "tailwind",
    "widget_tweaks",
    "crispy_forms",
    "theme",
    "parterre.apps.ParterreConfig",
    "utils.apps.UtilsConfig",
    "dashboard.apps.DashboardConfig",
    "artists.apps.ArtistsConfig",
    "playlists.apps.PlaylistsConfig",
    "explore.apps.ExploreConfig",
    "marketplace.apps.MarketplaceConfig",
]

MIDDLEWARE = [
    "core.middlewares.LogCSRFMiddleware"
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "core.middlewares.ForceDefaultLanguageMiddleware", # This will force the I18N machinery to always choose settings.LANGUAGE_CODE as the default initial language, unless another one is set via sessions or cookies
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_NAME'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = "it" # This will set the default language to Italian
LANGUAGES = [
    ('it', _('Italian')),
    ('en', _('English')),
]
LOCALE_PATHS = [BASE_DIR / "locale"]

TIME_ZONE = "UTC"

USE_I18N = True
USE_L10N = True

USE_TZ = True

LOGIN_REDIRECT_URL = "/dashboard"
LOGIN_URL = "/login/"

AUTH_USER_MODEL = "users.User"
AUTHENTICATION_BACKENDS = ["users.backends.CustomUserModelBackend"]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "theme/static"]

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = [
    "127.0.0.1",
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

PAGINATE_BY = 10

# Celery Configuration Options
CELERY_TIMEZONE = "Europe/Rome"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BROKER_URL = f'redis://{env("REDIS_HOST")}:{env("REDIS_PORT")}/0'
CELERY_RESULT_BACKEND = f'redis://{env("REDIS_HOST")}:{env("REDIS_PORT")}/0'

SPOTIFY_CLIENT_ID = env('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = env('SPOTIFY_CLIENT_SECRET')

SPOTIFY_PARTNER_CLIENT_VERSION = env('SPOTIFY_PARTNER_CLIENT_VERSION')
SPOTIFY_DC_COOKIE = env('SPOTIFY_DC_COOKIE')
SPOTIFY_KEY_COOKIE = env('SPOTIFY_KEY_COOKIE')

ALLOWED_HOSTS = env('ALLOWED_HOSTS', default="*").split(",")

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_S3_ENDPOINT_URL = 'https://parterre.fra1.digitaloceanspaces.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

AWS_MEDIA_LOCATION = 'media'
PUBLIC_MEDIA_LOCATION = 'media'
MEDIA_URL = f'{AWS_S3_ENDPOINT_URL}/{AWS_MEDIA_LOCATION}/'
DEFAULT_FILE_STORAGE = 'core.storage.MediaStorage'
AWS_S3_CUSTOM_DOMAIN = "parterre.fra1.cdn.digitaloceanspaces.com"


TELEGRAM_BOT_TOKEN = env('TELEGRAM_BOT_TOKEN')
TELEGRAM_TO_CHAT = env('TELEGRAM_TO_CHAT')

TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={TELEGRAM_TO_CHAT}&text="

CSRF_TRUSTED_ORIGINS = ['https://parterremusic.com']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}