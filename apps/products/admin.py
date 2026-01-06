from django.contrib import admin
from . import models

class ProductCategoryInline(admin.TabularInline):
    model = models.ProductCategory
    extra = 1

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductCategoryInline]

class VariantAttributeInline(admin.TabularInline):
    model = models.VariantAttribute
    extra = 1

class VariantImageInline(admin.TabularInline):
    model = models.VariantImage
    extra = 1

@admin.register(models.ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    inlines = [VariantAttributeInline, VariantImageInline]
    pass

@admin.register(models.Attribute)
class AttributeAdmin(admin.ModelAdmin):
    pass

# @admin.register(models.VariantAttribute)
# class VariantAttributeAdmin(admin.ModelAdmin):
#     pass

# @admin.register(models.VariantImage)
# class VariantImageAdmin(admin.ModelAdmin):
#     pass

@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(models.ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    pass
