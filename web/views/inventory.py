from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from inventory.models import StockItem, StockMovement
from catalog.models import ProductVariant, Product
from inventory.selectors import get_filtered_inventory

@login_required
def inventory_list_view(request, bus_id):
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    
    inventory_qs = get_filtered_inventory(business, request.GET)

    return render(request, 'web/workspace/inventory/list.html', {
        'business': business,
        'inventory': inventory_qs,
        'product_types': business.product_types.all(),
        'enabled_modules': business.enabled_modules.values_list('slug', flat=True),
        'filters': request.GET
    })

from django.db import transaction

@login_required
def stock_add_view(request, bus_id, variant_id):
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    variant = get_object_or_404(ProductVariant, product__business=business, id=variant_id)
    item = get_object_or_404(StockItem, variant=variant)

    if request.method == "POST":
        qty = int(request.POST.get('quantity', 0)) 
        
        with transaction.atomic():
            item.quantity += qty
            item.save()


            StockMovement.objects.create(
                business=business,
                variant=variant,
                quantity=qty,
                movement_type='IN',
                reason=request.POST.get('reason'),
                performed_by=request.user
            )

        messages.success(request, f"Запас товара {variant.product.name} пополнен на {qty} шт.")
        return redirect('web:inventory_list', bus_id=business.id)

    return render(request, 'web/workspace/inventory/add_stock.html', {
        'business': business,
        'variant': variant,
        'item': item,
        'enabled_modules': business.enabled_modules.values_list('slug', flat=True)
    })

