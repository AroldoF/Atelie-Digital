from django.contrib import admin
from . import models

class StoreImageInline(admin.TabularInline):
    model = models.StoreImage
    extra = 1

@admin.register(models.StoreCategory)
class StoreCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'store_category_id')
    search_fields = ('name',)

# 3. Configuração da Loja
@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin):
    inlines = [StoreImageInline] 
    
    list_display = ('name', 'user', 'category', 'phone_number', 'date_creation')
    list_filter = ('category', 'date_creation')
    search_fields = ('name', 'email', 'cnpj', 'user__username')
    autocomplete_fields = ['category']
