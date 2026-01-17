from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from apps.accounts.models import Address
from .models import Order, ProductVariant, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages


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

def removeCartItem(request, item_id):
    if request.method == 'POST':        
        item = get_object_or_404(CartItem, pk=item_id)

        cart_obj, _ = Cart.objects.new_or_get(request)

        if item.cart == cart_obj:
            item.delete()
            messages.success(request, 'Item removido do carrinho')
        else:
            messages.error(request, 'Você não tem permissão para remover este item.')

        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    return redirect('/')

def orders_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    context = {'order': order}
    return JsonResponse({'message': 'ainda não implemetado'})

def shipping(request):
    addresses = Address.objects.filter(user=request.user)
    context = {'addresses': addresses}
    return render(request, 'orders/shipping.html', context)

def checkout(request):
    return render(request, 'orders/checkout.html')

def approved(request):
    return render(request, 'orders/approved.html')
