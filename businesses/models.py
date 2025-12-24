from django.db import models

from users.models import User


class Module(models.Model):
    """Модули системы: 'inventory', 'catalog', 'sales', 'online_orders' и т.д."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name


class Business(models.Model):
    NICHES = (
        ('CLOTHES', 'Магазин одежды'),
        ('CAFE', 'Кофейня / Кафе'),
        ('BEAUTY', 'Салон красоты'),
        ('OTHER', 'Другое'),
    )   
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='owned_businesses')
    niche = models.CharField(max_length=20, choices=NICHES, default='CLOTHES')
    enabled_modules = models.ManyToManyField(Module, blank=True)
    plan = models.CharField(max_length=50, default='free')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name


class Staff(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='staff')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff_positions')
    role = models.CharField(max_length=50, choices=[
        ('admin', 'Админ'),
        ('manager', 'Менеджер'),
        ('master', 'Мастер'),
        ('employee', 'Сотрудник'),
    ])
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('business', 'user')


