from django.db.models import Sum, Count
from django.utils import timezone
from sales.models import Order, ProductVariant


def get_business_dashboard_stats(business):
    today = timezone.now().date()
    current_month = today.month
    current_year = today.year   

    today_stats = Order.objects.filter(
        business=business,
        created_at__date=today,
        status="PAID"
    ).aggregate(total_sum=Sum('total_amount'), count=Count('id'))
    
    month_stats = Order.objects.filter(
        business=business,
        status='PAID',
        created_at__month=current_month,
        created_at__year=current_year
    ).aggregate(total_sum=Sum('total_amount'), count=Count('id'))
    
    year_stats = Order.objects.filter(
        business=business,
        status='PAID',
        created_at__year=current_year
    ).aggregate(total_sum=Sum('total_amount'), count=Count('id'))

    top_5_variants = ProductVariant.objects.filter(
        product__business=business,
        order_variants__order__status='PAID'
    ).annotate(
        sales_count=Sum('order_variants__quantity')
    ).order_by('-sales_count')[:5] 

    return {
        'today_sum': today_stats['total_sum'] or 0,
        'today_count': today_stats['count'] or 0,
        
        'month_sum': month_stats['total_sum'] or 0,
        'month_count': month_stats['count'] or 0,
        
        'year_sum': year_stats['total_sum'] or 0,
        'year_count': year_stats['count'] or 0,
        
        'top_products': top_5_variants,
    }