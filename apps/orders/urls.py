from django.urls import path
from . import views

urlpatterns = [
    path("shopping_cart/", views.shopping_cart, name="shopping_cart"),
    path("order_checkout/", views.order_checkout, name="order_checkout")
]
