from django.test import TestCase
from decimal import Decimal
from users.models import User
from businesses.models import Business, Module
from catalog.models import ProductType, Product, ProductVariant
from inventory.models import StockItem
from sales.models import Order, OrderItem
from sales.services import process_order_sale

class SalesServicesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            first_name = 'test',
            telegram_id = '1234567890')
        
        self.module = Module.objects.create(
            name='Склад',
            slug='inventory'
        )

        self.business = Business.objects.create(
            name='testbus',
            owner=self.user
        )
        self.business.enabled_modules.add(self.module)

        self.p_type = ProductType.objects.create(
            business=self.business,
            name="Напитки",
            is_service=False)
        
        self.product = Product.objects.create(
            business=self.business,
            product_type=self.p_type,
            name="Кофе", is_service=False)

        self.variant = ProductVariant.objects.create(
            product=self.product,
            price=Decimal('150.00')
            )
        
        self.stock = StockItem.objects.get(business=self.business, variant=self.variant)
        self.stock.quantity = 10
        self.stock.save()
        
        self.order = Order.objects.create(
            business=self.business,
            seller=self.user,
            status='DRAFT')
        
    def test_process_order_sale(self):
        order_item = OrderItem.objects.create(
            order=self.order,
            variant=self.variant,
            quantity=2,
            price_at_purchase=Decimal('150.00')
        )
        process_order_sale(self.order.id)
        self.order.refresh_from_db()
        self.stock.refresh_from_db()
        self.assertEqual(self.order.status, 'PAID')
        self.assertEqual(self.stock.quantity, 8)