from django.db import models
from apps.core.models import Category
from apps.stores.models import Store

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField()
    is_active = models.BooleanField()

    class Meta:
        db_table = 'products'

class ProductVariant(models.Model):
    TYPE_CHOISES = [
        ('DEMAND', 'Demanda'),
        ('STOCK', 'Estoque')
    ]
    product_variant_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    sku = models.CharField(unique=True, max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=7, choices=TYPE_CHOISES, default='DEMAND')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(blank=True, null=True)
    production_days = models.IntegerField(blank=True, null=True)
    is_customizable = models.BooleanField()
    is_active = models.BooleanField()

    class Meta:
        db_table = 'product_variants'

class VariantImage(models.Model):
    variant_image_id = models.AutoField(primary_key=True)
    product_variant = models.ForeignKey(ProductVariant, models.CASCADE)
    image = models.ImageField()

    class Meta:
        db_table = 'variant_images'

class ProductCategory(models.Model):
    product_categories_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_categories', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_categories'
        unique_together = (('category', 'product'),)

class Attribute(models.Model):
    attribute_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'attributes'

    def __str__(self):
        return self.name

class VariantAttribute(models.Model):
    variant_attributes_id = models.AutoField(primary_key=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, related_name='variant_attributes', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    class Meta:
        db_table = 'variant_attributes'
        unique_together = (('attribute', 'product_variant'),)