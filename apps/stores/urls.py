from django.urls import path
from . import views

app_name = 'stores'

urlpatterns = [
    path('register/', views.Store_Register_View.as_view(), name='register'),

    # rotas dinâmicas
    path('<int:store_id>/dashboard/', views.dashboard, name='dashboard'),
    path('<int:store_id>/products/', views.artisan_products, name='stores_products'),
    path('<int:store_id>/orders/', views.artisan_orders, name='stores_orders'),

    # Rota genérica por último 
    path('<int:store_id>/', views.storeProfile, name='detail'),
]
