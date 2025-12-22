from django.db import models
from users.models import User
from businesses.models import Business


class ClientRelation(models.Model):
    """связь с моделями TelegramUser и Business"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_of')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='clients')
    status = models.CharField(max_length=32, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'business')
        verbose_name = "Клиент бизнеса"
        verbose_name_plural = "Клиенты бизнесов"

    def __str__(self):
        return f"{self.user} -> {self.business}"
