from django.db import models
from django.conf import settings
from apps.stores.models import Store
from apps.products.models import ProductVariant
from django.db.models import Sum, F, DecimalField, Q
from .utils import unique_order_code_generator
from django.db.models.signals import pre_save

class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        cart_obj = None
        new_obj = False
        user = request.user

        if cart_id:
            cart_obj = self.get_queryset().filter(cart_id=cart_id).first()

            if cart_obj and cart_obj.user and cart_obj.user != user:
                cart_obj = None

        if user.is_authenticated:
            cart_user = self.get_queryset().filter(user=user).first()

            if cart_obj and cart_user and cart_obj != cart_user:
                for item_session in cart_obj.items.all():
                    item_user = cart_user.items.filter(product_variant=item_session.product_variant).first()
                    
                    if item_user:
                        item_user.quantity += item_session.quantity
                        item_user.save()
                    else:
                        item_session.cart = cart_user
                        item_session.save()
                
                cart_obj.delete()
                cart_obj = cart_user

            elif cart_user:
                cart_obj = cart_user
            
            elif cart_obj:
                cart_obj.user = user
                cart_obj.save()

        else:
            if not cart_obj:
                cart_obj = self.get_queryset().filter(session_key=session_key).first()

        if not cart_obj:
            new_obj = True
            if user.is_authenticated:
                cart_obj = self.new(user=user)
            else:
                cart_obj = self.new(session_key=session_key)

        if request.session.get("cart_id") != cart_obj.cart_id:
            request.session["cart_id"] = cart_obj.cart_id

        return cart_obj, new_obj

    def new(self, user=None, session_key=None):
        return self.model.objects.create(user=user, session_key=session_key)

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return f'Cart {self.cart_id} - {self.user} {self.session_key}'
    
    @property
    def total_items(self):
        result = self.items.aggregate(total=Sum('quantity'))

        return result['total'] or 0
    
    @property
    def total(self):
        resultado = self.items.aggregate(
            valor_total=Sum(
                F('quantity') * F('product_variant__price'),
                output_field=DecimalField(),
                filter=Q(product_variant__is_active=True)
            )
        )
        return resultado['valor_total'] or 0
    
    class Meta:
        db_table = 'carts'
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    cart_item_id = models.AutoField(primary_key=True)
    product_variant = models.ForeignKey(ProductVariant, related_name='cart_products', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.quantity}x {self.product_variant} no Carrinho {self.cart.pk}'
    
    @property
    def price(self):
        return self.product_variant.price
    
    @property
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
    order_code = models.CharField(max_length=100, blank=True)
    transaction_id = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    store = models.ForeignKey(Store, related_name='orders', on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.PROTECT)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, default='PENDING')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_street = models.CharField(max_length=255)
    shipping_number = models.CharField(max_length=20)
    shipping_neigh = models.CharField(max_length=100)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=2)
    shipping_cep = models.CharField(max_length=8)
    shipping_complement = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.status} - {self.created_at}'
    
    class Meta:
        db_table = 'orders'
        
    def can_change_status(self):
        return self.status not in ['COMPLETED', 'CANCELLED']
    
    @property
    def get_total_calculado(self):
        # Soma o subtotal de todos os itens relacionados a este pedido
        return sum(item.subtotal() for item in self.items.all())

def pre_save_create_order_code(sender, instance, *args, **kwargs):
    if not instance.order_code:
        instance.order_code = unique_order_code_generator(instance)

pre_save.connect(pre_save_create_order_code, sender = Order)

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


