from django.db import models
from django.conf import settings
from apps.core.models import Category

class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='stores', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    phone_number = models.CharField(unique=True, max_length=15)
    cnpj = models.CharField(unique=True, max_length=14, blank=True, null=True)
    email = models.EmailField(unique=True, max_length=255)
    image = models.ImageField()
    banner = models.ImageField()

    class Meta:
        db_table = 'stores'

class StoreImage(models.Model):
    store_image_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    image = models.TextField()

    class Meta:
        db_table = 'store_images'

class StoreCategory(models.Model):
    store_categories_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, related_name='store_categories', on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name='store_categories', on_delete=models.CASCADE)

    class Meta:
        db_table = 'store_categories'
        unique_together = (('category', 'store'),)


