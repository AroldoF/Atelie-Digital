from django.urls import path
from . import views

urlpatterns = [
    path('store-profile/', views.storeProfile, name='storeProfile'),
    path('dashboard/', views.dashboard, name='storeProfile'),
    path('register/', views.Store_Register_View.as_view(), name='register'),
    path('artisan-products/', views.artisan_products, name='artisan_products'),
]
