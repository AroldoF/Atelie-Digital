from django.contrib import admin
from . import models

@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin):
    pass

@admin.register(models.StoreImage)
class StoreImageAdmin(admin.ModelAdmin):
    pass

@admin.register(models.StoreCategory)
class StoreCategoryAdmin(admin.ModelAdmin):
    pass
