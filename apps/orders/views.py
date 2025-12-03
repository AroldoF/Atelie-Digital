from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from apps.accounts.models import Address
from .models import Order

def orders_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    context = {'order': order}
    return JsonResponse({'message': 'ainda não implemetado'})

def shipping(request):
    addresses = Address.objects.filter(user=request.user)
    context = {'addresses': addresses}
    return render(request, 'orders/shipping.html', context)

def shopping_cart(request):
    return render(request, 'orders/shopping_cart.html')

def checkout(request):
    return render(request, 'orders/checkout.html')

def approved(request):
    return render(request, 'orders/approved.html')
