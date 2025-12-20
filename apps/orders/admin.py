from django.contrib import admin
from . import models

class OrderProductInline(admin.TabularInline):
    model = models.OrderProduct
    extra = 1

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]

# @admin.register(models.OrderProduct)
# class BuyAdmin(admin.ModelAdmin):
#     pass


