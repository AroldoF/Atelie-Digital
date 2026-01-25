from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views import View
from django.db.models import Avg, Count, Q, Exists, OuterRef
from django.contrib.postgres.search import (SearchVector,SearchQuery,SearchRank,TrigramSimilarity)
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from decimal import Decimal
from django.db import transaction
from django.contrib import messages
from .forms import ProductForm, VarianteInlineFormSet
from .models import Product, Favorite, ProductReview
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import DeleteView
from apps.stores.models import Store
from apps.orders.models import OrderProduct


CATEGORY_KEYWORDS = {
    "tecidos": ["faixa","faixinhas", "laço","laços", "tiara", "tecido"],
    "madeira": ["madeira","caixa", "caixinha", "madeira"],
    "ceramica": ["cerâmica","vaso", "caneca", "prato"],
}


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = "products/confirm_delete.html"
    context_object_name = "product"
    permission_required = 'products.delete_product'

    def get_queryset(self):
        """usuário só pode deletar produtosda própria loja"""
        store = get_object_or_404(
            Store,
            store_id=self.kwargs["store_id"],
            user=self.request.user
        )
        return Product.objects.filter(store=store)

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        product_name = product.name

        product.delete()

        messages.success(
            request,
            f'O produto "{product_name}" foi excluído com sucesso.'
        )

        return redirect(
            "stores:stores_products",
            store_id=self.kwargs["store_id"]
        )

    

    def get_success_url(self):
        return reverse(
            "stores:stores_products",
            kwargs={"store_id": self.kwargs["store_id"]}
        )

def detail_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Lógica de variantes e disponibilidade 
    variants = product.variants.filter(is_active=True)
    variant_id = request.GET.get('variant')

    variant = None
    if variant_id:
        variant = product.variants.filter(product_variant_id=variant_id).first()
    
    if not variant:
        variant = variants.first()
     # Produto disponível se o pai estiver ativo e houver variante ativa
    is_available = product.is_active and variant is not None and  variant.is_active

    # Lógica de Avaliações e "Comprador Verificado"
    
    # Subconsulta: Verifica se o autor da review possui um OrderProduct deste produto
    # Isso reflete o sucesso do pagamento mostrado na sua imagem de checkout
    user_purchases = OrderProduct.objects.filter(
        order__user=OuterRef('user'),
        product_variant__product=product
    )

    # informação de compra
    all_reviews_qs = product.reviews.annotate(
        user_has_purchased=Exists(user_purchases)
    ).order_by("-created_at")

    # Cálculos de médias (usando a query anotada)
    reviews_data = all_reviews_qs.aggregate(
        media=Avg('rating'), 
        total=Count('review_id')
    )
    
    rating_average = reviews_data['media'] or 0.0
    reviews_count = reviews_data['total'] or 0
    
    # Composição das estrelas (gráfico de barras)
    stars_composition = []
    for i in range(5, 0, -1):
        count_for_star = all_reviews_qs.filter(rating=i).count()
        percentage = (count_for_star / reviews_count * 100) if reviews_count > 0 else 0
        stars_composition.append({
            'star_number': i,
            'count': count_for_star,
            'percentage': round(percentage, 1)
        })

    # LIMITE PROGRESSIVO DE COMENTÁRIOS
    DEFAULT_LIMIT = 3
    reviews_limit = int(request.GET.get("reviews_limit", DEFAULT_LIMIT))
    reviews = all_reviews_qs[:reviews_limit]

    has_more_reviews = reviews_limit < all_reviews_qs.count()
    next_reviews_limit = reviews_limit + DEFAULT_LIMIT

    # LIMITE DE QUANTIDADE PELO ESTOQUE
    max_quantity = None

    if variant and variant.type == 'STOCK':
        max_quantity = variant.stock
    #simular desconto
    REFERENCE_PRICE = Decimal('55.00')
    discount_percent = 0
    if variant and variant.price < REFERENCE_PRICE:
        discount_percent = round((REFERENCE_PRICE - variant.price) / REFERENCE_PRICE * 100)
     # Verifica se deve mostrar a área de personalização
    show_personalization = False
    if variant:
        show_personalization = variant.is_customizable or variant.type == 'DEMAND'

 
    context = {
        'product': product,
        'variant': variant,
        'variants': variants,
        'is_available': is_available,
        'unavailable_message': "Este produto está indisponível no momento." if not is_available else "",
        'reviews': reviews, # Cada review aqui tem o atributo .user_has_purchased
        'rating_average': round(rating_average, 1),
        'reviews_count': reviews_count,
        'stars_composition': stars_composition,
        
        "has_more_reviews": has_more_reviews,
        "next_reviews_limit": next_reviews_limit,
        'max_quantity': max_quantity,
        'show_personalization': show_personalization,
        'discount_percent': discount_percent,
    }
    
    return render(request, 'products/detail.html', context)


def search_product(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category")

    if category:
        category = category.lower()

    products = Product.objects.filter(is_active=True)
    active_filter = category if category else "todos"

    # Busca textual
    if query:
        vector = (
            SearchVector("name", weight="A", config="portuguese") +
            SearchVector("description", weight="B", config="portuguese")
        )
        search_query = SearchQuery(query, config="portuguese")

        products = products.annotate(
            rank=SearchRank(vector, search_query),
            similarity=(
                TrigramSimilarity("name", query) +
                TrigramSimilarity("description", query)
            ),
        ).filter(
            Q(rank__gt=0) | Q(similarity__gt=0.2)
        )

    # Filtro por categoria
    if category and category in CATEGORY_KEYWORDS:
        include_q = Q()
        for keyword in CATEGORY_KEYWORDS[category]:
            include_q |= Q(name__icontains=keyword)
            include_q |= Q(description__icontains=keyword)

        products = products.filter(include_q)

    # Ordenação
    if query:
        products = products.order_by("-rank", "-similarity")
    else:
        products = products.order_by("name")

    products = products.distinct()

    # paginação
    paginator = Paginator(products, 4) 
    page_number = request.GET.get("page")
    products_page = paginator.get_page(page_number)

    return render(request, "products/search.html",{ "query": query,"products_page": products_page, "active_filter": active_filter,})


class ProductCreateView(PermissionRequiredMixin, View):
    permission_required = 'products.add_product'
    template_name = "products/register.html"
    
    def get(self, request):
        context = {
            "product_form": ProductForm(prefix="product"),
            "variant_formset": VarianteInlineFormSet(
                instance=None,
                prefix="variants"
            ),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        product_form = ProductForm(
            request.POST,
            request.FILES,
            prefix="product"
        )

        variant_formset = VarianteInlineFormSet(
            request.POST,
            request.FILES,
            prefix="variants"
        )

        # 1️⃣ Validação básica
        if not product_form.is_valid() or not variant_formset.is_valid():
            return render(request, self.template_name, {
                'product_form': product_form,
                'variant_formset': variant_formset
            })

        store = request.user.stores.first()


        with transaction.atomic():
            # 2️⃣ Produto
            product = product_form.save(commit=False)
            product.store = store
            product.save()

            # 3️⃣ Vincula produto ao formset
            variant_formset.instance = product

            # 4️⃣ Salva TODAS as variantes (VALIDADAS)
            variant_formset.save()


        messages.success(request, "Produto cadastrado com sucesso!")
        return redirect("stores:stores_products", store_id=product.store.pk)

class ProductUpdateView(PermissionRequiredMixin, View):
    permission_required = 'products.change_product'
    template_name = "products/edit.html"

    def get_object(self, product_id):
        return get_object_or_404(Product, pk=product_id)

    def get(self, request, product_id):
        product = self.get_object(product_id)

        return render(request, self.template_name, context={
            'product_form': ProductForm(instance=product, prefix='product'),
            "variant_formset": VarianteInlineFormSet(instance=product,prefix="variants"),
        })
    
    def post(self, request, product_id):
        product = self.get_object(product_id)

        product_form = ProductForm(
            request.POST,
            request.FILES,
            instance=product,
            prefix='product'
        )

        variant_formset = VarianteInlineFormSet(
            request.POST,
            request.FILES,
            instance=product,
            prefix='variants'
        )

        if not product_form.is_valid() or not variant_formset.is_valid():
            for form in variant_formset.forms:
                delete_value = form.cleaned_data.get('DELETE') if form.is_bound and form.is_valid() else form.data.get(form.add_prefix('DELETE'))
                if delete_value in [True, 'on', '1']:
                    # Adiciona flag para template
                    form.hidden_in_template = True
                    # Garante que o DELETE hidden vai como 'on'
                    if 'DELETE' in form.fields:
                        form.fields['DELETE'].initial = 'on'


            return render(request, self.template_name, {
                'product_form': product_form,
                'variant_formset': variant_formset
            })

        with transaction.atomic():
            product_form.save()

            variant_formset.save()

            for form in variant_formset.forms:
                if hasattr(form, "nested_attributes"):
                    for attr_form in form.nested_attributes.forms:
                        delete = attr_form.cleaned_data.get('DELETE', False)
                        attr_id = attr_form.cleaned_data.get('variant_attributes_id')  # hidden field
                        if delete and attr_id:
                            from .models import VariantAttribute
                            try:
                                VariantAttribute.objects.get(pk=attr_id.pk).delete()
                            except VariantAttribute.DoesNotExist:
                                pass



        messages.success(request, "Produto editado com sucesso!")
        return redirect("stores:stores_products", store_id=product.store.pk)


@require_POST
def toggle_favorite(request, product_id):
    if not request.user.is_authenticated:
        response = HttpResponse(status=401)
        response["HX-Redirect"] = reverse("accounts:login")
        return response

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

        
@login_required
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
