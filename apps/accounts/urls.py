from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("settings/user", views.settings_user, name="settings_user"),
    path("settings/address", views.settings_address, name="settings_address"),
    path("settings/artisian", views.settings_artisian, name="settings_artisian"),
    path('addresses/register', views.AddressesRegister.as_view(), name='addresses')
]
