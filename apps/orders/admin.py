from django.contrib import admin
from . import models

class OrderProductInline(admin.TabularInline):
    model = models.OrderProduct
    extra = 1

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]


class CartItemInline(admin.TabularInline):
    model = models.CartItem
    extra = 1

@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]

# @admin.register(models.OrderProduct)
@admin.register(models.OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    pass

# class BuyAdmin(admin.ModelAdmin):
#     pass


