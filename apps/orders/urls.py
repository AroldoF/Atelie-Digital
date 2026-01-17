from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # path("list/", views.list, name="list"),
    path('add/', views.addToCart, name='add'),
    path("cart/", views.viewCart, name="cart"),
    path('shipping/', views.shipping, name='shipping'),
    path("checkout/", views.checkout, name="checkout"),
    path("approved/", views.approved, name="approved"),
 
    path('<int:order_id>/', views.orders_detail, name='detail'),

    # Carrinho
    path('<int:item_id>/remove/', views.removeCartItem, name='remove_item'),
    path('<int:item_id>/update/<str:action>/', views.updateCartItem, name='update_item')

]