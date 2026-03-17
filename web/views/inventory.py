from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from inventory.models import StockItem, StockMovement
from catalog.models import ProductVariant, Product
from inventory.selectors import get_filtered_inventory, get_filtered_movements
from django.core.paginator import Paginator
from django.db.models import F
@login_required
def inventory_list_view(request, bus_id):
    """This func shows your inventory"""

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
def stock_add_view(request, bus_id, variant_id=None):
    """This func adds the items on the inventory"""
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    

    selected_variant_id = request.GET.get('variant')
    if selected_variant_id:
        try:
            selected_variant_id = int(selected_variant_id)
        except ValueError:
            selected_variant_id = None

    if request.method == "POST":
        v_id = request.POST.get('variant')
        variant = get_object_or_404(ProductVariant, id=v_id, product__business=business)
        qty = int(request.POST.get('quantity', 0))
        
        with transaction.atomic():
            item, created = StockItem.objects.get_or_create(business=business, variant=variant)
            from django.db.models import F
            item.quantity = F('quantity') + qty
            item.save()

            StockMovement.objects.create(
                business=business,
                variant=variant,
                quantity=qty,
                movement_type='IN',
                reason=request.POST.get('reason'),
                performed_by=request.user
            )

        messages.success(request, "Склад успешно обновлен!")
        return redirect('web:inventory_list', bus_id=business.id)

    all_variants = ProductVariant.objects.filter(
        product__business=business, 
        product__is_service=False
    ).select_related('product')

    return render(request, 'web/workspace/inventory/add_stock.html', {
        'business': business,
        'variants': all_variants,
        'selected_variant_id': selected_variant_id,
        'enabled_modules': business.enabled_modules.values_list('slug', flat=True)
    })

@login_required
def inventory_history_view(request, bus_id):
    """This func shows your business item history"""

    business = get_object_or_404(request.user.owned_businesses, id=bus_id)

    history_list = get_filtered_movements(business, request.GET)

    paginator = Paginator(history_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'web/workspace/inventory/history.html', {
        'business': business,
        'page_obj': page_obj, 
        'enabled_modules': business.enabled_modules.values_list('slug', flat=True),
        'filters': request.GET
    })