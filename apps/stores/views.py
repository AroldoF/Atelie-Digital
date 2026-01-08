from django.shortcuts import render
from django.views import View
from .forms import StoreCreationForm, StoreCategories_Form

# Create your views here.

def storeProfile(request):
    return render(request, 'stores/storeProfile.html')

def dashboard(request):
    return render(request, 'stores/dashboard.html', {'active_page': 'dashboard'})

def artisan_products(request):
    return render(request, 'stores/artisan_products_table.html', {'active_page': 'products'})

def artisan_orders(request):
    return render(request, 'stores/artisan_orders_table.html', {'active_page': 'orders'})

class StoreCreationView(View):
    def get(self, request):
        context = {
            'form': StoreCreationForm(),
            'form_category': StoreCategories_Form()
        }
        return render(request, 'stores/register.html', context)