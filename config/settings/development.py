from .base import *
from dotenv import load_dotenv
import os

load_dotenv()

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
DB_PASSWORD =  os.getenv('DB_PASSWORD')
# === БД (уже отлично) ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hubly_db',
        'USER': 'root',
        'PASSWORD': DB_PASSWORD,
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# === Debug Toolbar — пока полностью выключен (чтобы не падал) ===
# Раскомментируешь только когда я дам тебе идеальную настройку через 2 минуты

# INSTALLED_APPS += [
#     'debug_toolbar',
#     'django_extensions',
# ]

# MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

# INTERNAL_IPS = ['127.0.0.1', 'localhost']

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

print("→ Development настройки загружены успешно (MySQL + hubly_db)")