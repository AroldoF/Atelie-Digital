from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('search/', views.search_product, name='search'), 
    path('register/', views.ProductCreateView.as_view(), name='register'),
    # path('favorites/', views.favoriteProduct, name='favorites'), não deveria estar aqui

    path('favorite/<int:product_id>/', views.toggle_favorite, name='toggle_favorite'),

    # rotas dinâmicas por ultimo
    path('<int:product_id>/', views.detail_product, name='detail'),
    path("products/<int:product_id>/review/",views.submit_review,name="submit_review"),
    # path('edit/<int:product_id>/', views.product_edit, name='edit'),
    
]
