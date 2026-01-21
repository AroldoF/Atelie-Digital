from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    # Autenticação
    path("login/", views.UserLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("register/", views.register, name="register"),

    # Perfil (Esta é a rota da task atual)
    path("me/", views.profile, name="profile"),
    
    # Configurações
    path("me/edit/", views.profileEdit, name="profile_edit"),
    path("me/artisan/", views.becomeArtisian, name="settings_artisian"),

    # Placeholders futuros
    path('me/orders/', views.usersOrders, name='orders'),
    path('me/favorites/', views.favoriteProduct, name='favorites'),
    
    # Endereços
    path('me/addresses/', views.addressesList, name='addresses'),
    path('me/addresses/register', views.AddressesRegister.as_view(), name='addresses_register'),
    path("me/addresses/<int:address_id>/edit/", views.addressEdit, name="settings_address"),
]