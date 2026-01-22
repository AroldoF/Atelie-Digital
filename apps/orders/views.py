from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from apps.accounts.models import Address
from .models import Order, ProductVariant, Cart, CartItem, OrderProduct
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.core.exceptions import ValidationError


@require_POST 
def addToCart(request):
    if request.method == 'POST':
        variant_id = request.POST.get('variant_id')
        quantity = int(request.POST.get('quantity'))
        
        variant = get_object_or_404(ProductVariant, pk=variant_id)
        cart_obj, _ = Cart.objects.new_or_get(request)

        cart_item = CartItem.objects.filter(cart=cart_obj, product_variant=variant).first()
        quantity_in_cart = cart_item.quantity if cart_item else 0

        if variant.type == 'STOCK':
            total_desired = quantity_in_cart + quantity
            
            if total_desired > variant.stock:
                remaining = variant.stock - quantity_in_cart
                
                if remaining > 0:
                    messages.error(request, f'Estoque insuficiente. Você já tem {quantity_in_cart} no carrinho e só restam mais {remaining} unidades.')
                else:
                    messages.error(request, 'Você já adicionou todo o estoque disponível deste produto ao seu carrinho.')
                
                return redirect(request.META.get('HTTP_REFERER', '/'))

        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            CartItem.objects.create(
                cart=cart_obj, 
                product_variant=variant, 
                quantity=quantity
            )

        messages.success(request, f'Produto adicionado ao carrinho!')
        return redirect(request.META.get('HTTP_REFERER', '/'))
        
    return redirect('/')

def viewCart(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)

    items = cart_obj.items.select_related('product_variant').all()

    context = {'cart': cart_obj, 'items': items}
    
    return render(request, 'orders/shopping_cart.html', context)

def updateCartItem(request, item_id, action):
    if request.method == 'POST':        
        item = get_object_or_404(CartItem, pk=item_id)

        cart_obj, _ = Cart.objects.new_or_get(request)

        if item.cart == cart_obj:
            if not item.product_variant.is_active:
                messages.error(request, 'Este produto não está mais disponível para venda.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
            
            if action == 'increase':
                quantity_desired = item.quantity + 1
                if item.product_variant.type == 'STOCK' and quantity_desired > item.product_variant.stock:
                    messages.warning(request, 'O estoque máximo já foi adicionado ao seu carrinho.')
                else:
                    item.quantity += 1
                    item.save()

            elif action == 'decrease':
                new_quantity = item.quantity - 1

                if new_quantity <= 0:
                    item.delete()
                    messages.warning(request, 'Item removido do carrinho')
                else:
                    item.quantity -= 1
                    item.save()
            else:
                messages.error(request, 'Você não pode realizar esta ação.')

        else:
            messages.error(request, 'Você não tem permissão para alterar este item.')

        return redirect(request.META.get('HTTP_REFERER', '/'))

    return redirect('/')

def removeCartItem(request, item_id):
    if request.method == 'POST':        
        item = get_object_or_404(CartItem, pk=item_id)

        cart_obj, _ = Cart.objects.new_or_get(request)

        if item.cart == cart_obj:
            item.delete()
            messages.warning(request, 'Item removido do carrinho')
        else:
            messages.error(request, 'Você não tem permissão para remover este item.')

        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    return redirect('/')

@login_required
def shipping(request):
    # puxar os dados do carrinho
    cart_obj, _ = Cart.objects.new_or_get(request)

    if not cart_obj.items.exists():
        messages.warning(request, "O carrinho está vazio!")
        return redirect('orders:cart')        
    else:
        # listar os endereços existentes
        addresses = Address.objects.filter(user=request.user)

        # validar status e quantidade de produto em estoque
        for item in cart_obj.items.all():
            product = item.product_variant
            if not product.is_active:
                messages.warning(request, f'O produto {product.description} não está disponivel para venda. Remova-o do carrinho e prossiga com a compra')
                return redirect('orders:cart')
                
            if product.type == 'STOCK':
                if product.stock < item.quantity:
                    messages.warning(request, f'O produto {product.description} esgotou o estoque. Remova-o do carrinho e prossiga com a compra.')
                    return redirect('orders:cart')

    context = {'addresses': addresses, 'cart_obj': cart_obj}

    return render(request, 'orders/shipping.html', context)

@login_required
def payment(request):
    if request.method == 'POST':
        address_id = request.POST.get('shipping_address')

        cart_obj, _ = Cart.objects.new_or_get(request)

    context = {'address_id':address_id, 'cart': cart_obj}

    return render(request, 'orders/payment.html', context)

@login_required
def checkout(request):
    if request.method == 'POST':
        address_id = request.POST.get('shipping_address')
        
        try:
            address = Address.objects.get(pk=address_id, user=request.user)
        except Address.DoesNotExist:
            messages.error(request, "Endereço selecionado é inválido.")
            return redirect('orders:shipping')

        cart_obj, _ = Cart.objects.new_or_get(request)
        cart_items = cart_obj.items.select_related('product_variant', 'product_variant__product__store').all()

        if not cart_items.exists():
            messages.warning(request, "Seu carrinho está vazio.")
            return redirect('orders:cart')

        # Cria um dicionário: { <Store A>: [Item1, Item2], <Store B>: [Item3] }
        items_by_store = {}
        for item in cart_items:
            store = item.product_variant.product.store
            if store not in items_by_store:
                items_by_store[store] = []
            items_by_store[store].append(item)

        try:
            with transaction.atomic():
                
                # Iteramos sobre as lojas para criar um pedido para cada uma
                for store, items_list in items_by_store.items():
                    
                    # Calcula o total específico desta loja
                    store_total = sum(item.subtotal for item in items_list)

                    # Criação do Pedido 
                    order = Order.objects.create(
                        store=store,
                        user=request.user,
                        status='PENDING',
                        total_amount=store_total,
                        shipping_street=address.street,
                        shipping_number=address.number,
                        shipping_neigh=address.neighborhood, 
                        shipping_city=address.city,
                        shipping_state=address.state,
                        shipping_cep=address.cep,
                        shipping_complement=address.complement
                    )

                    # Processamento dos Itens
                    for item in items_list:
                        product = item.product_variant

                        # Validação 1: Produto Ativo
                        if not product.is_active:
                            raise ValidationError(f"O produto {product.description} não está mais disponível.")

                        # Validação 2: Estoque
                        if product.type == 'STOCK' and product.stock < item.quantity:
                            raise ValidationError(f"Estoque insuficiente para {product.description}.")

                        # Baixa de Estoque Segura (Concurrency)
                        if product.type == 'STOCK':
                            product.stock = F('stock') - item.quantity
                            product.save()

                        # Criação do Item do Pedido
                        OrderProduct.objects.create(
                            order=order,
                            product_variant=product,
                            quantity=item.quantity,
                            price_at_purchase=product.price 
                        )

                # Deletar os itens do carrinho
                cart_obj.items.all().delete() 

            messages.success(request, "Pedido realizado com sucesso!")
            return redirect('orders:approved') 

        except ValidationError as e:
            messages.warning(request, e.message)
            return redirect('orders:cart')
            
        except Exception as e:
            messages.error(request, "Ocorreu um erro ao processar seu pedido. Nada foi cobrado.")
            return redirect('orders:cart')

    return redirect('orders:cart')

def approved(request):
    return render(request, 'orders/approved.html')


def orders_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    context = {'order': order}
    return JsonResponse({'message': 'ainda não implemetado'})


