from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from sales.models import Order, OrderItem
from businesses.models import Business
from catalog.models import ProductVariant
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from sales.services import process_order_sale, refund_order_sale
from sales.selectors import get_filtered_orders


@login_required
def order_list_view(request, bus_id):
    """This func shows all orders list"""
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    orders_qs = get_filtered_orders(business, request.GET)
    paginator = Paginator(orders_qs, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
     
    return render(request, 'web/workspace/sales/order_list.html', {
        'business': business,
        'page_obj': page_obj,
        'filters': request.GET,
        'enabled_modules': business.enabled_modules.values_list('slug', flat=True)
    })

@login_required
def order_create_view(request, bus_id):
    """This func crates a new draft order"""
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    new_order = Order.objects.create(
        business=business,
        seller=request.user,
        customer_phone="",
    )
    messages.success(request, f"Открыт новый чек #{new_order.id:05d}")
    return redirect('web:order_detail', bus_id=business.id, order_id=new_order.id)

@login_required
def order_detail_view(request, bus_id, order_id):
    """This func shows details your orders"""
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    order = get_object_or_404(Order, business=business, id=order_id)

    items = order.items.select_related('variant__product').all()

    available_variants = ProductVariant.objects.filter(
        product__business=business, 
        is_active=True
    ).select_related('product').prefetch_related('stock_items')

    return render(request, 'web/workspace/sales/order_detail.html', {
        'business': business,
        'order': order,
        'items': items,
        'available_variants': available_variants,
        'enabled_modules': business.enabled_modules.values_list('slug', flat=True)
    })

@login_required
@require_POST
def add_item_to_order_view(request, bus_id, order_id, variant_id):
    """This func adds new product variant in the order"""
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    order = get_object_or_404(Order, business=business, id=order_id)
    if order.status != 'DRAFT':
        messages.success(request, "Нельзя изменить уже оплаченный заказ!")
        return redirect('web:order_detail', bus_id=business.id, order_id=order.id)
    

    variant = get_object_or_404(ProductVariant, product__business=business, id=variant_id)

    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        variant=variant,
        defaults={
            'quantity': 1, 
            'price_at_purchase': variant.price
        }
    )

    if not created:
        order_item.quantity += 1
        order_item.save()
        
    total = sum(item.price_at_purchase * item.quantity for item in order.items.all())
    order.total_amount = total
    order.save()
    
    return redirect('web:order_detail', bus_id=business.id, order_id=order.id)

@login_required
def order_delete_view(request, bus_id, order_id):
    """This func deletes selected order"""
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    order = get_object_or_404(Order, business=business, id=order_id)

    if order.status == "PAID":
        messages.error(request, "Ошибка: нельзя удалить уже оплаченный чек! (Функция возврата в разработке)")
        return redirect('web:order_detail', bus_id=business.id, order_id=order.id)
    
    order.delete()
    messages.success(request, "Чек успешно удален!")
    return redirect('web:order_list', bus_id=business.id)

@login_required
@require_POST
def order_pay_view(request, bus_id, order_id):
    """This func pays the order"""
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    order = get_object_or_404(Order, business=business, id=order_id)
    
    if not order.items.exists():
        messages.error(request, "Нельзя оплатить пустой чек! Добавьте товары.")
        return redirect('web:order_detail', bus_id=business.id, order_id=order.id)
        
    try:
        process_order_sale(order.id)
        messages.success(request, f"Чек #{order.id:05d} успешно оплачен! Склад обновлен.")
    except ValidationError as e:
        error_msg = e.message if hasattr(e, 'message') else e.messages[0]
        messages.error(request, error_msg)
        
    return redirect('web:order_detail', bus_id=business.id, order_id=order.id)

@login_required
@require_POST
def remove_item_from_order_view(request, bus_id, order_id, item_id):
    """This func removes the product variant from order"""
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    order = get_object_or_404(Order, business=business, id=order_id)
    
    if order.status != 'DRAFT':
        messages.error(request, "Нельзя изменить оплаченный заказ!")
        return redirect('web:order_detail', bus_id=business.id, order_id=order.id)
        
    item = get_object_or_404(OrderItem, id=item_id, order=order)
    
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
        
    total = sum(i.price_at_purchase * i.quantity for i in order.items.all())
    order.total_amount = total
    order.save()
    
    return redirect('web:order_detail', bus_id=business.id, order_id=order.id)

@login_required
@require_POST
def clear_order_view(request, bus_id, order_id):
    """This func clears your order"""
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    order = get_object_or_404(Order, business=business, id=order_id)

    if order.status != 'DRAFT':
        messages.error(request, 'Невозможно удалить данные оплаченного или отклоненного чека!')
        return redirect('web:order_detail', bus_id=business.id, order_id=order.id)
    
    if not order.items.exists():
        messages.error(request, 'Чек пустой, дейсвие невозможно!')
        return redirect('web:order_detail', bus_id=business.id, order_id=order.id)
    order.items.all().delete()
    order.total_amount=0
    order.save()
    messages.success(request, 'Чек успешно очищен!')
    return redirect('web:order_detail', bus_id=business.id, order_id=order.id)

@login_required
@require_POST
def cancel_order_view(request, bus_id, order_id):
    """This func swaps status the orders to CANCELLED"""
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    order = get_object_or_404(Order, business=business, id=order_id)
    try:
        refund_order_sale(order.id)
        messages.success(request, f"Чек #{order.id:05d}, возврат успешно совершен!")
    except ValidationError as e:
        error_msg = e.message if hasattr(e, 'message') else e.messages[0]
        messages.error(request, error_msg)

    return redirect('web:order_detail', bus_id=business.id, order_id=order.id)