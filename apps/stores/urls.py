from django.urls import path
from . import views

urlpatterns = [
     path('store-profile/', views.storeProfile, name='storeProfile'),
     path('dashboard/', views.dashboard, name='storeProfile'),
]