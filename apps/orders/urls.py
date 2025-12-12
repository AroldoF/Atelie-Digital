from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # path("list/", views.list, name="list"),
    path("cart/", views.shopping_cart, name="cart"),
    path('shipping/', views.shipping, name='shipping'),
    path("checkout/", views.checkout, name="checkout"),
    path("approved/", views.approved, name="approved"),

    # rotas dinâmicas por ultimo
    path('<int:order_id>/', views.orders_detail, name='detail'),
]