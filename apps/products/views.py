from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views import View
from .forms import Product_Form, Product_Variant_Form, Attributes_Form
from .models import Product, Favorite
from django.http import HttpResponse

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

@require_POST
@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        favorite.delete()
    response = HttpResponse()
    # Redireciona de volta para a mesma página
    response["HX-Redirect"] = request.META.get("HTTP_REFERER", "/")
    return response
    return redirect(request.META.get('HTTP_REFERER', '/'))