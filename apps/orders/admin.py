from django.contrib import admin
from . import models

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(models.OrderProduct)
class BuyAdmin(admin.ModelAdmin):
    pass


