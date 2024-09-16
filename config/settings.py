import os
from datetime import timedelta, datetime
from pathlib import Path

import pytz
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure--t_4)3!-#**93az!mv%le!5$nciz99ff0f^-6#h!ecu@-m**gs'
DEBUG = True
ALLOWED_HOSTS = []

load_dotenv(BASE_DIR / '.env')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework_simplejwt',
    'django_celery_beat',
    'drf_yasg',
    'corsheaders',

    'authen_drf',
    'habit',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

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

LANGUAGE_CODE = 'ru-Ru'
TIME_ZONE = "Asia/Yakutsk"
USE_I18N = True
USE_TZ = True
NULLABLE = {"null": True, "blank": True}
AUTH_USER_MODEL = 'authen_drf.User'

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=180),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

# СТАТИЧЕСКИЕ ФАЙЛЫ
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

# ПОЧТА
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# CELERY
CELERY_BROKER_URL = os.getenv("CELERY_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_URL")
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_BEAT_SCHEDULE = {
    'check_habit_time': {
        'task': 'habit.tasks.check_habit_time',
        'schedule': timedelta(hours=1),
        'start_time': datetime.now(pytz.timezone(TIME_ZONE))
    },
}

CORS_ALLOWED_ORIGINS = [
    os.getenv('SITE_ADDR'),  # Замените на адрес вашего фронтенд-сервера
]

CSRF_TRUSTED_ORIGINS = [
    os.getenv('SITE_ADDR'),  # Замените на адрес вашего фронтенд-сервера
    # и добавьте адрес бэкенд-сервера
]

CORS_ALLOW_ALL_ORIGINS = False
