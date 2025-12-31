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
from django.db.models import Avg,Count
from apps.utils.purchases import user_bought_product


def detail_product(request, product_id):

    product = get_object_or_404(Product, pk=product_id)
    
    # Lógica de variantes e disponibilidade
    variants = product.variants.filter(is_active=True)
    variant_id = request.GET.get('variant')

    if variant_id:
        variant = product.variants.filter(product_variant_id=variant_id).first()
    else:
        variant = variants.first()

    # Produto disponível se o pai estiver ativo e houver variante ativa
    is_available = product.is_active and variant is not None and variant.is_active



    # Verifica se o usuário comprou o produto
    # has_bought = user_bought_product(request.user, product) 
    has_bought = True # para teste


    # Cálculos de Avaliações 
    reviews_data = product.reviews.aggregate(
        media=Avg('rating'), 
        total=Count('review_id')
    )
    
    rating_average = reviews_data['media'] or 0.0
    reviews_count = reviews_data['total'] or 0
    
    #  Listagem e Composição da Nota 
    reviews = product.reviews.all().order_by('-created_at')
    stars_composition = []
    
    for i in range(5, 0, -1):  # Loop de 5 até 1 estrela
        count_for_star = reviews.filter(rating=i).count()
        # Calcula a porcentagem para a barra de progresso
        percentage = (count_for_star / reviews_count * 100) if reviews_count > 0 else 0
        
        stars_composition.append({
            'star_number': i,
            'count': count_for_star,
            'percentage': round(percentage, 1)
        })

  
    # LIMITE PROGRESSIVO DE COMENTÁRIOS
   
    DEFAULT_LIMIT = 3
    reviews_limit = int(request.GET.get("reviews_limit", DEFAULT_LIMIT))

    all_reviews_qs = product.reviews.all().order_by("-created_at")
    reviews = all_reviews_qs[:reviews_limit]

    has_more_reviews = reviews_limit < all_reviews_qs.count()
    next_reviews_limit = reviews_limit + DEFAULT_LIMIT

    context = {
        'product': product,
        'variant': variant,
        'variants': variants,
        'is_available': is_available,
        'unavailable_message': "Este produto está indisponível no momento." if not is_available else "",
        'reviews': reviews,
        'rating_average': round(rating_average, 1),
        'reviews_count': reviews_count,
        'stars_composition': stars_composition,
        'has_bought': has_bought,
        
        # controle do botão
        "has_more_reviews": has_more_reviews,
        "next_reviews_limit": next_reviews_limit,
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


        
@login_required(login_url="accounts:login")
def submit_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    variant_id = request.GET.get("variant")

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        if rating:
            ProductReview.objects.create(
                product=product,
                user=request.user,
                rating=int(rating),
                comment=comment,
            )

    if variant_id:
        return redirect(f"/products/{product_id}/?variant={variant_id}")

    return redirect("products:detail", product_id=product_id)
