from django.contrib import admin
from .models import User, Address

@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Address)
class AddressesAdmin(admin.ModelAdmin):
    list_display = ['street', 'user']
