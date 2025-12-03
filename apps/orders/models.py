from django.db import models
from django.conf import settings
from apps.stores.models import Store
from apps.products.models import ProductVariant

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, related_name='orders', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'orders'

class Buy(models.Model):
    buy_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, related_name='buys', on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, related_name='buys', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'buys'

