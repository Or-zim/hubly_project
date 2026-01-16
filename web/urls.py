from django.urls import path
from . import views
urlpatterns = [
    path('login/<uuid:token>/', views.magic_login, name='magic_login'),
    path('', views.index_view, name='index'),
    path('create-business/', views.create_business_wizard, name='create_business'),
]

app_name = 'web'