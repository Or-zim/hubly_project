from django.urls import path
from .views import common, catalog, business, inventory
urlpatterns = [
    path('login/<uuid:token>/', common.magic_login, name='magic_login'),
    path('', common.index_view, name='index'),
    path('create-business/', business.create_business_wizard, name='create_business'),
    path('b/<int:bus_id>/', business.business_main_view, name='business_main'),
    path('b/<int:bus_id>/delete/', business.delete_business, name='delete_business'),
    path('b/<int:bus_id>/catalog/product_type_list/', catalog.product_type_list_view, name='product_type_list'),
    path('b/<int:bus_id>/catalog/create_product_type/', catalog.product_type_add_view, name='create_product_type'),
    path('b/<int:bus_id>/catalog/types/delete/<int:scheme_id>/', catalog.delete_product_type, name='product_type_delete'),
    path('b/<int:bus_id>/catalog/add/<int:scheme_id>/', catalog.product_add_view, name='product_add'),
    path('b/<int:bus_id>/catalog/', catalog.product_type_index_list, name='catalog_index'),
    path('b/<int:bus_id>/catalog/type/<int:type_id>/', catalog.product_list_by_type_view, name='product_list_by_type'),
    path('b/<int:bus_id>/catalog/product/delete/<int:prod_id>/', catalog.delete_product, name='delete_product'),
    path('b/<int:bus_id>/catalog/product/<int:prod_id>/', catalog.product_detail_view, name='product_detail'),
    path('b/<int:bus_id>/catalog/product/<int:prod_id>/variant/add/', catalog.variant_add_view, name='variant_add'),
    path('b/<int:bus_id>/catalog/product/<int:prod_id>/variant/delete/<int:variant_id>/', catalog.variant_delete, name='variant_delete'),
    path('b/<int:bus_id>/catalog/product/<int:prod_id>/variant/edit/<int:variant_id>/', catalog.variant_edit_view, name='variant_edit'),
    path('b/<int:bus_id>/inventory/', inventory.inventory_list_view, name='inventory_list'),
    path('b/<int:bus_id>/inventory/add/', inventory.stock_add_view, name='inventory_add'),
    path('b/<int:bus_id>/inventory/history/', inventory.inventory_history_view, name='inventory_history'),
]

app_name = 'web'