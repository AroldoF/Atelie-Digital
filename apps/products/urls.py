from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('register/', views.Product_Register_View.as_view(), name='register'),
    # path('searchProducts/', views.searchProduct, name='searchProduct'), # não deveria estar aqui
    # path('favorites/', views.favoriteProduct, name='favorites'), não deveria estar aqui

    # rotas dinâmicas por ultimo
    path('<int:product_id>/', views.detailProduct, name='detail'),
    
]
