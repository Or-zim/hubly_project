from django.db.models import F, Q
from .models import Order

def get_filtered_orders(business, filters):
    """This func filters your business orders"""
    queryset = Order.objects.filter(business=business)

    status = filters.get('status')
    if status and status != "ALL":
        queryset = queryset.filter(status=status)

    search = filters.get('search')
    if search:
        try:
            order_id = int(search)
            queryset = queryset.filter(Q(id=order_id) | Q(customer_phone__icontains=search))
        except ValueError: 
            queryset = queryset.filter(customer_phone__icontains=search)



    date = filters.get('date')
    if date:
        queryset = queryset.filter(created_at__date=date)
    
    return queryset
