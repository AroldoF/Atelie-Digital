from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('register/', views.Product_Register_View.as_view(), name='register'),
    path('search/', views.searchProduct, name='search'), 
    # path('favorites/', views.favoriteProduct, name='favorites'), não deveria estar aqui

    path('favorite/<int:product_id>/', views.toggle_favorite, name='toggle_favorite'),

    # rotas dinâmicas por ultimo
    path('<int:product_id>/', views.detailProduct, name='detail'),
    
]
