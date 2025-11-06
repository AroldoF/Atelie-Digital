from django.db import models
from apps.accounts.models import Users
from apps.stores.models import Stores
from apps.products.models import ProductVariants

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Stores, related_name='orders', on_delete=models.CASCADE)
    user = models.ForeignKey(Users, related_name='orders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'

class Buys(models.Model):
    buy_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, related_name='buys', on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariants, related_name='buys', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'buys'

