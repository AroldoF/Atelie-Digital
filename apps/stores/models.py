from django.db import models
from apps.accounts.models import Users
from apps.core.models import Categories

class Stores(models.Model):
    store_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, related_name='stores', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    phone_number = models.CharField(unique=True, max_length=15)
    cnpj = models.CharField(unique=True, max_length=14, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'stores'

class StoreCategories(models.Model):
    store_categories_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    store = models.ForeignKey(Stores, related_name='store_categories', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'store_categories'
        unique_together = (('category', 'store'),)


