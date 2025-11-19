from django.urls import path
from . import views

template_name = "products"

urlpatterns = [
    path('register/', views.Product_Register_View.as_view(), name='register'),
    path('searchProducts/', views.searchProduct, name='searchProduct'),
    path('detailProducts/', views.detailProduct, name='detailProducts'),
    path('favoriteProduct/', views.favoriteProduct, name='favoriteProduct'),
    
]
