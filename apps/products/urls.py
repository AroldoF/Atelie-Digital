from django.urls import path
from . import views

template_name = "products"

urlpatterns = [
    path('register/', views.Product_Register_View.as_view(), name='register')
]
