from django.db import models
from apps.core.models import Categories
from apps.stores.models import Stores

class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Stores, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.TextField()
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'products'

class ProductVariants(models.Model):
    product_variant_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, related_name='variants', on_delete=models.CASCADE)
    sku = models.CharField(unique=True, max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_customizable = models.BooleanField()
    type = models.CharField(max_length=7)
    stock = models.IntegerField(blank=True, null=True)
    production_days = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'product_variants'

class ProductCategories(models.Model):
    product_categories_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name='product_categories', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'product_categories'
        unique_together = (('category', 'product'),)

class Attributes(models.Model):
    attribute_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'attributes'

class VariantAttributes(models.Model):
    variant_attributes_id = models.AutoField(primary_key=True)
    attribute = models.ForeignKey(Attributes, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariants, related_name='variant_attributes', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'variant_attributes'
        unique_together = (('attribute', 'product_variant'),)