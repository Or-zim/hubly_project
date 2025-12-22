from django.urls import path
from . import views
urlpatterns = [
    path('login/<uuid:token>/', views.magic_login, name='magic_login'),
    path('', views.dashboard, name='dashboard'), 
    path('create-business/', views.create_business_view, name='create_business'),
]

app_name = 'web'