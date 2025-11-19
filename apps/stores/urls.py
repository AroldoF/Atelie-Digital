from django.urls import path
from . import views

urlpatterns = [
     path('store-profile/', views.storeProfile, name='storeProfile'),
     path('dashboard/', views.dashboard, name='dashboard'),
     path('artisan-products/', views.artisan_products, name='artisan_products'),
     path('artisan-orders/', views.artisan_orders, name='artisan_orders'),
]
