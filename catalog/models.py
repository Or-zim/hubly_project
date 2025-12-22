from django.db import models
from django.conf import settings
from businesses.models import Business


class Category(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products')
    name = models.CharField(max_length=120)
    sku = models.CharField(max_length=64, blank=True, help_text="Артикул/внутренний код модели (общий для всех размеров).")
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Базовая цена, если у вариантов нет своей.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=32, blank=True, help_text="Размер: XS, S, M, L, 42, 44 и т.д.")
    color = models.CharField(max_length=64, blank=True, help_text="Цвет: Black, White, Blue и т.п.")
    sku = models.CharField(max_length=64, blank=True, help_text="Артикул / штрихкод конкретного варианта.")
    price_override = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Если указана, используется вместо базовой цены товара."
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'size', 'color')