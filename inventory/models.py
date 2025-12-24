from django.db import models
from catalog.models import ProductVariant
from businesses.models import Business
from users.models import User


class StockItem(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='stock_items')
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество на складе")
    min_threshold = models.PositiveIntegerField(default=5, verbose_name="Минимальный порог")
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('business', 'variant')

class StockMovement(models.Model):
    MOVEMENT_TYPES = (
        ('IN', 'Приход (Поставка)'),
        ('OUT', 'Продажа'),
        ('CORRECTION', 'Корректировка (Инвентаризация)'),
        ('RETURN', 'Возврат от клиента'),
    )
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)