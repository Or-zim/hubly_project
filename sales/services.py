from django.db import transaction
from django.core.exceptions import ValidationError
from inventory.models import StockItem, StockMovement
from .models import Order

def process_order_sale(order_id):
    """
    Сервис для обработки продажи: списывает товары со склада 
    и создает записи о движении.
    """

    with transaction.atomic():
        order = Order.objects.select_for_update().get(id=order_id)

        if order.status == 'PAID':
            raise ValidationError("Этот заказ уже оплачен и списан.")
        
        for item in order.items.all():
            stock = StockItem.objects.filter(business=order.business, variant=item.variant).select_for_update().first()

            if not stock or stock.quantity < item.quantity:
                raise ValidationError(
                    f"Недостаточно товара: {item.variant}. "
                    f"На складе: {stock.quantity if stock else 0}, требуется: {item.quantity}"
                )
            
            from django.db.models import F
            stock.quantity = F('quantity') - item.quantity
            stock.save()

            StockMovement.objects.create(
                business=order.business,
                variant=item.variant,
                movement_type='OUT',
                quantity=-item.quantity,
                reason=f"Продажа по заказу #{order.id}",
                performed_by=order.seller
                )
        order.status = 'PAID'
        order.save()
        
    return order