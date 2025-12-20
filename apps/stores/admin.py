from django.contrib import admin
from . import models

class StoreImageInline(admin.TabularInline):
    model = models.StoreImage
    extra = 1

class StoreCategoryInline(admin.TabularInline):
    model = models.StoreCategory
    extra = 1


@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin):
    inlines = [StoreCategoryInline, StoreImageInline]
