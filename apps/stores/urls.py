from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.Store_Register_View.as_view(), name='register')
]
