from django.urls import path
from . import views

urlpatterns = [
    path("shopping_cart/", views.shopping_cart, name="shopping_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("checkout/approved/", views.approved, name="approved")
]
