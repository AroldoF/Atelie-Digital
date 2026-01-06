from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views import View
from .forms import Product_Form, Product_Variant_Form, Attributes_Form
from .models import Product, Favorite
from django.http import HttpResponse
from .models import Product, ProductVariant
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from .forms import Product_Form, Product_Variant_Form, Attributes_Form,ProductReviewForm
from .models import Product, ProductVariant, ProductReview
from django.shortcuts import get_object_or_404
from django.db.models import Avg


def detail_product(request, product_id):
   
    product = get_object_or_404(Product, pk=product_id)
    variants = product.variants.filter(is_active=True)
    variant_id = request.GET.get('variant')
    if variant_id:
        
        variant = product.variants.filter(product_variant_id=variant_id).first()
    else:
        
        variant = variants.first()

 
    is_available = product.is_active and variant is not None and variant.is_active

    unavailable_message = None
    if not is_available:
        unavailable_message = "Este produto está indisponível no momento."

    
    reviews = product.reviews.all().order_by('-created_at')

   
    context = {
        'product': product,
        'variant': variant,
        'variants': variants,
        'is_available': is_available,
        'unavailable_message': unavailable_message,
        'reviews': reviews,
    }
    
    return render(request, 'products/detail.html', context)


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


@login_required(login_url="login")
def submit_review(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id)
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        if rating:
            # update_or_create permite que o usuário atualize a nota se já tiver avaliado
            ProductReview.objects.update_or_create(
                product=product, 
                user=request.user,
                defaults={'rating': int(rating), 'comment': comment}
            )
        
    return redirect('products:detail', product_id=product_id)
