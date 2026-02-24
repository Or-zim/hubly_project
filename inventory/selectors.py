from django.db.models import F, Q
from .models import StockItem

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