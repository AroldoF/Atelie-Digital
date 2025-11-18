from django.shortcuts import render

# Create your views here.
def shopping_cart(request):
    return render(request, 'orders/shopping_cart.html')

def checkout(request):
    return render(request, 'orders/checkout.html')
