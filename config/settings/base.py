# myproject/settings/base.py
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ------------------- СЕКРЕТЫ -------------------
SECRET_KEY = config('DJANGO_SECRET_KEY', default='django-insecure-замени-на-свой-длинный-ключ!!!')

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='localhost,127.0.0.1,[::1],.localhost', cast=Csv())

# ------------------- ПРИЛОЖЕНИЯ -------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'users',
    'clients',
    'transactions',
    'notifications',
    'businesses',
    'Hubly_bot',
    'web',
    'catalog',
    'inventory',
    'sales'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# ------------------- БАЗА ДАННЫХ — SQLite везде! -------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',   # ← файл будет прямо в корне проекта
    }
}

# ------------------- СТАТИКА И МЕДИА -------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ------------------- ОСТАЛЬНОЕ -------------------
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

# ==========================================
# НАСТРОЙКИ REST FRAMEWORK & CORS & JWT
# ==========================================

# Настройки CORS (Cross-Origin Resource Sharing)
# На этапе разработки разрешаем запросы с любых фронтендов
CORS_ALLOW_ALL_ORIGINS = True 

# В продакшене потом поменяешь на False и укажешь конкретные домены:
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "https://tvoy-frontend-domen.com",
# ]

# Настройки Django REST Framework
REST_FRAMEWORK = {
    # По умолчанию все эндпоинты будут требовать авторизации (кроме тех, где мы явно разрешим)
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    # Способ авторизации (мы переходим на JWT вместо стандартных сессий)
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# Настройки времени жизни токенов (необязательно, но полезно для удобства)
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60), # Access токен живет час
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),    # Refresh токен (для обновления) живет неделю
    'AUTH_HEADER_TYPES': ('Bearer',),               # Формат заголовка: "Authorization: Bearer <token>"
}