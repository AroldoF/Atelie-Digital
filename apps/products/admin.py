from django.contrib import admin
from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(models.ProductVariant)
class Admin(admin.ModelAdmin):
    pass

@admin.register(models.Attribute)
class AttributeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.VariantAttribute)
class VariantAttributeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.VariantImage)
class VariantImageAdmin(admin.ModelAdmin):
    pass

@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass
