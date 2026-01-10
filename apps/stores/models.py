from django.db import models
from django.conf import settings
from apps.core.models import Category
from apps.utils.storage import store_gallery_upload_path, store_image_upload_path, banner_upload_path

class StoreCategory(models.Model):
    store_category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'store_categories'

class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='stores', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(StoreCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='stores')
    phone_number = models.CharField(unique=True, max_length=15)
    date_creation = models.DateTimeField(auto_now_add=True)
    cnpj = models.CharField(unique=True, max_length=14, blank=True, null=True)
    email = models.EmailField(unique=True, max_length=255)
    image = models.ImageField(upload_to=store_image_upload_path)
    banner = models.ImageField(upload_to=banner_upload_path)

    def __str__(self):
        return f'{self.name} (ID: {self.store_id})'

    class Meta:
        db_table = 'stores'

class StoreImage(models.Model):
    store_image_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=store_gallery_upload_path)

    def __str__(self):
        return f'Imagem da loja: {self.store.name}'

    class Meta:
        db_table = 'store_images'






