from django.db import models
from django.conf import settings
from apps.stores.models import Store
from apps.products.models import ProductVariant

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Carrinho {self.cart_id} - {self.created_at}'
    
    class Meta:
        db_table = 'carts'
        verbose_name = 'Carrinho'
        verbose_name_plural = 'Carrinhos'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    cart_item_id = models.AutoField(primary_key=True)
    product_variant = models.ForeignKey(ProductVariant, related_name='cart_products', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.quantity}x {self.product_variant} no Carrinho {self.cart.pk}'
    
    def subtotal(self):
        return self.product_variant.price * self.quantity

    class Meta:
        db_table = 'cart_items'
        unique_together = ('cart', 'product_variant')

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('PENDING', 'Pendente'),
        ('IN_PROGRESS', 'Em andamento'),
        ('COMPLETED', 'Concluído'),
        ('CANCELLED', 'Cancelado'),
    ]

    order_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, related_name='orders', on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.PROTECT)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, default='PENDING')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.status} - {self.created_at}'
    
    class Meta:
        db_table = 'orders'

class OrderProduct(models.Model):
    order_product_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, related_name='order_items', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.order}, {self.product_variant}'
    
    def subtotal(self):
        # Usa o preço CONGELADO no momento da compra
        return self.price_at_purchase * self.quantity
    
    def save(self, *args, **kwargs):
        # Garante que o preço seja salvo automaticamente na criação se não for passado
        if not self.price_at_purchase:
            self.price_at_purchase = self.product_variant.price
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'order_products'

