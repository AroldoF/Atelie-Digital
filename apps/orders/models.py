from django.db import models
from django.conf import settings
from apps.stores.models import Store
from apps.products.models import ProductVariant

class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ('PENDING', 'Pendente'),
        ('IN_PROGRESS', 'Em andamento'),
        ('COMPLETED', 'Conclu�do'),
        ('CANCELLED', 'Cancelado'),
    ]

    order_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, related_name='orders', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    type = models.CharField(choices=ORDER_TYPE_CHOICES)
    created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.type} - {self.created_at}'
    
    class Meta:
        db_table = 'orders'

class OrderProduct(models.Model):
    order_product_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, related_name='buys', on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, related_name='buys', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.order}, {self.product_variant}'

    class Meta:
        db_table = 'order_products'

