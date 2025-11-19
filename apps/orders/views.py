from django.shortcuts import render
from apps.accounts.models import Addresses

def confirmAddress(request):
    user_id = request.user.id
    addresses = Addresses.objects.filter(user=user_id)
    context = {'addresses': addresses}
    return render(request, 'orders/confirm-address.html', context)

# Create your views here.
def list(request):
    return render(request, "orders/list.html")

def shopping_cart(request):
    return render(request, 'orders/shopping_cart.html')

def checkout(request):
    return render(request, 'orders/checkout.html')

def approved(request):
    return render(request, 'orders/approved.html')
