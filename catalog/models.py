from django.db import models
from django.conf import settings
from businesses.models import Business
from django.db.models.signals import post_save
from django.dispatch import receiver


class ProductType(models.Model):
    """
    Тип товара (Шаблон). Определяет, какие поля будут у товара.
    Например: "Одежда" (поля: Размер, Цвет), "Обувь" (Размер, Шипы).
    """
    business = models.ForeignKey(
        'businesses.Business', 
        on_delete=models.CASCADE, 
        related_name='product_types'
    )
    name = models.CharField(max_length=100)
    fields = models.JSONField(default=list)

    def __str__(self):
        return f"{self.name} ({self.business.name})"

class Product(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product_type = models.ForeignKey(
        ProductType, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='products'
    )

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=64, blank=True, null=True, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    attributes = models.JSONField(default=dict) 
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        attrs = ", ".join([f"{k}: {v}" for k, v in self.attributes.items()])
        return f"{self.product.name} ({attrs})"
    
    def save(self, *args, **kwargs):
        if not self.sku:
            super().save(*args, **kwargs)
            self.sku = f"{self.id:08d}" 
            kwargs['force_insert'] = False
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

@receiver(post_save, sender=ProductVariant)
def create_stock_item(sender, instance, created, **kwargs):
    from inventory.models import StockItem
    if created:
        StockItem.objects.create(
            business=instance.product.business,
            variant=instance,
            quantity=0
        )