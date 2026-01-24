from django.urls import path
from . import views

app_name = 'stores'

urlpatterns = [
    path('register/', views.StoreCreateView.as_view(), name='register'),

    # rotas dinâmicas
    path('<int:store_id>/dashboard/', views.dashboard, name='dashboard'),
    path('<int:store_id>/products/', views.artisan_products, name='stores_products'),
    path('<int:store_id>/orders/', views.artisan_orders, name='stores_orders'),
    path('<int:store_id>/orders/<int:order_id>/',views.artisan_order_detail,name='artisan_order_detail'),

    # Rota genérica por último 
    path('<int:store_id>/', views.store_detail, name='detail'),
]
