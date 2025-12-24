from django.db import models
from catalog.models import ProductVariant
from businesses.models import Business
from users.models import User


class Order(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Черновик'),
        ('PAID', 'Оплачен'),
        ('CANCELLED', 'Отменен'),
    )
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='orders')
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sales')
    customer_phone = models.CharField(max_length=32, blank=True, null=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='DRAFT')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Заказ #{self.id} в {self.business.name}"
    


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.variant} x {self.quantity}"