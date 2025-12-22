from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True, db_index=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_blocked = models.BooleanField(default=False)
    def __str__(self):
        return self.username or f"TG: {self.telegram_id}"


class AuthToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # Ссылка живет 2 минуты
        return timezone.now() < self.created_at + timedelta(minutes=2)

    def __str__(self):
        return f"Token for {self.user} ({self.created_at})"