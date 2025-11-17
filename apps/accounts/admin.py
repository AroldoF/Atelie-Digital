from django.contrib import admin
from .models import Users, Addresses

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Addresses)
class AddressesAdmin(admin.ModelAdmin):
    list_display = ['street', 'user']
