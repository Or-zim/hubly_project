# myproject/settings/production.py
from .base import *

DEBUG = False

# Обязательно переопредели в .env на сервере!
SECRET_KEY = config('DJANGO_SECRET_KEY')  # без дефолта — будет ошибка, если забудешь
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='localhost', cast=Csv())
# Безопасность
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Сжатая статика через Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

print("→ Используется production.py (SQLite + максимальная безопасность)")