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
    # Captura os dados enviados pelo formulário do outro app
        variant_id = request.POST.get('variant_id')
        quantity = int(request.POST.get('quantity'))

        # Busca a variante no banco (validação básica)
        variant = get_object_or_404(ProductVariant, pk=variant_id)

        # Criar/Pegar o carrinho
        
        cart_obj, created = Cart.objects.new_or_get(request)

        # Criar/Pegar os itens do carrinho
        item, created = CartItem.objects.get_or_create(cart=cart_obj, product_variant=variant, defaults={'quantity': quantity})
        if not created:
            item.quantity += quantity
            item.save()

        # 3. Redireciona o usuário 
        messages.success(request, "Produto adicionado ao carrinho")
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    return redirect('/')

def viewCart(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)

    items = cart_obj.items.select_related('product_variant').all()

    context = {'cart': cart_obj, 'items': items}
    
    return render(request, 'orders/shopping_cart.html', context)

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
