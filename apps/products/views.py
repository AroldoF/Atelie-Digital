from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .forms import Product_Form, Product_Variant_Form, Attributes_Form


def detailProduct(request):
    return render(request, 'products/detailProduct.html')

def searchProduct(request):
    return render(request, 'products/searchProduct.html')


class Product_Register_View(View):
    def get(self, request):
        context = {
            'form_products': Product_Form(),
            'form_variant': Product_Variant_Form(),
            'form_attribute': Attributes_Form()
        }
        return render(request, 'products/register.html', context)

