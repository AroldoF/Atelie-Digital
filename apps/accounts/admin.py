from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "user_id",
        "username",
        "name",
        "email",
        "cpf",
        "phone_number",
        "is_active",
        "is_staff",
        "is_artisan",
    ]
    search_fields = ["username", "email", "name", "cpf"]
    list_filter = ["is_staff", "is_artisan", "is_active"]


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "bio"]
    search_fields = ["user__username", "user__email"]
    readonly_fields = ["user"]  # opcional, se você não quiser alterar o user diretamente


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        "address_id",
        "user",
        "street",
        "number",
        "neighborhood",
        "city",
        "state",
        "cep",
        "is_main",
    ]
    search_fields = ["street", "city", "state", "user__username", "user__email"]
    list_filter = ["state", "is_main"]
