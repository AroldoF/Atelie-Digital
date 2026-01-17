from django.db import models
from django.conf import settings
from apps.stores.models import Store
from apps.products.models import ProductVariant
from django.db.models import Sum, F, DecimalField, Q

class CartManager(models.Manager):
    def new_or_get(self, request):
        # 1. Garante que existe uma sessão criada no navegador
        # Se for um usuário novo, a session_key pode ser None, então criamos forçadamente.
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        cart_obj = None
        new_obj = False

        # 2. Lógica se o usuário estiver LOGADO
        if request.user.is_authenticated:
            # Tenta buscar um carrinho já existente deste usuário
            # Usamos filter().first() para evitar erro caso não exista (retorna None)
            cart_obj = self.get_queryset().filter(user=request.user).first()
            
            # Se o usuário não tem carrinho salvo, mas tem um carrinho da sessão atual (anônimo)
            if not cart_obj:
                cart_from_session = self.get_queryset().filter(session_key=session_key).first()
                if cart_from_session:
                    # "Adotamos" o carrinho anônimo para o usuário logado
                    cart_obj = cart_from_session
                    cart_obj.user = request.user
                    cart_obj.session_key = None 
                    cart_obj.save()
        
        # 3. Lógica se o usuário for ANÔNIMO (ou se logado não tinha nada e nada na sessão)
        if not cart_obj:
            # Tenta pegar o carrinho pela chave da sessão
            cart_obj = self.get_queryset().filter(session_key=session_key).first()
            
            # Se o usuário logou agora e não tinha carrinho nenhum, vincula a ele.
            # Se for anônimo, continua anônimo.
            if cart_obj and request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()

        # 4. Se ainda não achou nada (nem no user, nem na session), CRIA UM NOVO
        if not cart_obj:
            new_obj = True
            if request.user.is_authenticated:
                cart_obj = self.new(user=request.user)
            else:
                cart_obj = self.new(session_key=session_key)

        return cart_obj, new_obj

    def new(self, user=None, session_key=None):
        # Cria efetivamente o carrinho com os dados passados
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

