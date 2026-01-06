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


from django.shortcuts import render, get_object_or_404
from .models import Product

def detail_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    variants = product.variants.filter(is_active=True)
    variant_id = request.GET.get("variant")

    if variant_id:
        variant = get_object_or_404(
            ProductVariant,
            pk=variant_id,
            product=product,
            is_active=True
        )
    else:
        variant = variants.first()

    reviews = product.reviews.select_related("user").order_by("-created_at")

    review_form = ProductReviewForm()

    context = {
        "product": product,
        "variants": variants,
        "variant": variant,
        "reviews": reviews,
        "review_form": review_form,
    }

    return render(request, "products/detail.html", context)


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
    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review, created = ProductReview.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={
                    "rating": form.cleaned_data["rating"],
                    "comment": form.cleaned_data["comment"],
                }
            )
    return redirect("detail_product", product_id=product_id)

