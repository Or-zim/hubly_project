from django.db.models import F, Q
from .models import StockItem, StockMovement

def get_filtered_inventory(business, filters: dict):
    """
    Универсальная функция для получения остатков с фильтрацией.
    filters - это словарь из request.GET (search, type, stock и т.д.)
    """
    queryset = StockItem.objects.filter(
        business=business
    ).select_related('variant__product__product_type')

    search = filters.get('search')
    if search:
        queryset = queryset.filter(variant__product__name__icontains=search)

    type_id = filters.get('type')
    if type_id:
        queryset = queryset.filter(variant__product__product_type_id=type_id)

    stock_status = filters.get('stock')
    if stock_status == 'out':
        queryset = queryset.filter(quantity__lte=0)
    elif stock_status == 'low':
        queryset = queryset.filter(quantity__gt=0, quantity__lte=F('min_threshold'))
        
    return queryset


def get_filtered_movements(business, filters: dict):
    """
    Получение истории движений с фильтрацией.
    """
    queryset  = StockMovement.objects.filter(business=business).select_related('variant__product__product_type', 'performed_by')
    
    date = filters.get('date')
    if date:
        queryset = queryset.filter(created_at__date=date)

    type_movement = filters.get('type_movement')
    if type_movement and type_movement != 'all':
        queryset = queryset.filter(movement_type=type_movement.upper())

    return queryset