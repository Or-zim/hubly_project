from django.db import transaction
from django.core.exceptions import ValidationError
from inventory.models import StockItem, StockMovement
from .models import Order

def process_order_sale(order_id):
    """
    The payment service checks balances, writes off goods,
    creates movement records, and changes the status of a check.
    """
    with transaction.atomic():
        order = Order.objects.select_for_update().get(id=order_id)

        if order.status == 'PAID':
            raise ValidationError("Этот чек уже был оплачен ранее.")
        
        has_inventory = order.business.enabled_modules.filter(slug='inventory').exists()
        
        for item in order.items.select_related('variant__product').all():
            
            if item.variant.product.is_service or not has_inventory:
                continue

            stock = StockItem.objects.filter(
                business=order.business, 
                variant=item.variant
            ).select_for_update().first()

            if not stock or stock.quantity < item.quantity:
                raise ValidationError(
                    f"Недостаточно товара: {item.variant.product.name}. "
                    f"На складе: {stock.quantity if stock else 0} шт., требуется: {item.quantity} шт."
                )
            
            from django.db.models import F
            stock.quantity = F('quantity') - item.quantity
            stock.save()

            StockMovement.objects.create(
                business=order.business,
                variant=item.variant,
                movement_type='SALE',
                quantity=-item.quantity,
                reason=f"Продажа по чеку #{order.id:05d}",
                performed_by=order.seller
            )
            
        order.status = 'PAID'
        order.save()
        
    return order

def refund_order_sale(order_id):
    """
    The servise creates the returned orders 
    """
    with transaction.atomic():
        order = Order.objects.select_for_update().get(id=order_id)

        if order.status != 'PAID':
            raise ValidationError("Можно оформить возврат только для оплаченного чека.")
        
        has_inventory = order.business.enabled_modules.filter(slug='inventory').exists()
        
        for item in order.items.select_related('variant__product').all():
            
            if item.variant.product.is_service or not has_inventory:
                continue

            stock = StockItem.objects.filter(
                business=order.business, 
                variant=item.variant
            ).select_for_update().first()

            if stock:
                from django.db.models import F
                stock.quantity = F('quantity') + item.quantity
                stock.save()

                StockMovement.objects.create(
                    business=order.business,
                    variant=item.variant,
                    movement_type='RETURN',       
                    quantity=item.quantity,       
                    reason=f"Возврат по чеку #{order.id:05d}",
                    performed_by=order.seller
                )
            
        order.status = 'CANCELLED'
        order.save()
        
    return order
