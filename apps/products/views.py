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
from django.db.models import Q
from django.contrib.postgres.search import (SearchVector,SearchQuery,SearchRank,TrigramSimilarity)
from django.core.paginator import Paginator
from django.contrib.auth.mixins import PermissionRequiredMixin
from decimal import Decimal
from django.db import transaction
from django.contrib import messages
from .forms import Product_Form, Attributes_Form, VarianteInlineFormSet
from .models import Product, Favorite, ProductVariant, VariantAttribute, Attribute, VariantImage
from django.http import HttpResponse, JsonResponse
import json

CATEGORY_KEYWORDS = {
    "tecidos": ["faixa","faixinhas", "laço","laços", "tiara", "tecido"],
    "madeira": ["madeira","caixa", "caixinha", "madeira"],
    "ceramica": ["cerâmica","vaso", "caneca", "prato"],
}

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
        'reviews': reviews,
        'rating_average': round(rating_average, 1),
        'reviews_count': reviews_count,
        'stars_composition': stars_composition,
        'has_bought': has_bought,
        
        # controle do botão
        "has_more_reviews": has_more_reviews,
        "next_reviews_limit": next_reviews_limit,
        # qtd maxima
        'max_quantity':max_quantity,

        #para a exibição do chat
        'show_personalization': show_personalization,
        #simulação de desconto
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
            "product_form": Product_Form(prefix="product"),
            "variant_formset": VarianteInlineFormSet(
                instance=None,
                prefix="variants"
            ),
            # Usado APENAS como ponte para Attribute
            "attribute_variant": Attributes_Form(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        product_form = Product_Form(
            request.POST,
            request.FILES,
            prefix="product"
        )

        variant_formset = VarianteInlineFormSet(
            request.POST,
            request.FILES,
            prefix="variants"
        )

        variants_json = request.POST.get("variants_json")

        # 1️⃣ Validação básica
        if not product_form.is_valid() or not variant_formset.is_valid():
            return render(
                request,
                self.template_name,
                self._context_with_errors(product_form, variant_formset)
            )

        if not variants_json:
            product_form.add_error(None, "Adicione ao menos uma variante.")
            return render(
                request,
                self.template_name,
                self._context_with_errors(product_form, variant_formset)
            )

        try:
            variants_data = json.loads(variants_json)
        except json.JSONDecodeError:
            product_form.add_error(None, "Dados das variantes inválidos.")
            return render(
                request,
                self.template_name,
                self._context_with_errors(product_form, variant_formset)
            )

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

            # 5️⃣ Atributos (usando a ordem do formset)
            for form, variant_data in zip(variant_formset.forms, variants_data):
                variant = form.instance

                imagens = form.cleaned_data.get('images')

                if imagens:
                    for image in imagens:
                        VariantImage.objects.create(
                            product_variant = variant,
                            image = image
                        )
                for attr_data in variant_data.get("attributes", []):
                    attr_form = Attributes_Form(
                        data={
                            "attribute": attr_data["attribute_id"],
                            "value": attr_data["value"],
                        }
                    )

                    if not attr_form.is_valid():
                        form.add_error(
                            None,
                            f"Atributo inválido: {attr_form.errors.as_text()}"
                        )
                        return render(
                            request,
                            self.template_name,
                            self._context_with_errors(product_form, variant_formset)
                        )

                    variant_attr = attr_form.save(commit=False)
                    variant_attr.product_variant = variant
                    variant_attr.save()


        messages.success(request, "Produto cadastrado com sucesso!")
        return redirect("index")

    def _context_with_errors(self, product_form, variant_formset):
        return {
            "product_form": product_form,
            "variant_formset": variant_formset,
            "attribute_variant": Attributes_Form(),
        }

import json
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

def product_edit(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'GET':
        product_form = Product_Form(instance=product, prefix="product")
        variant_formset = VarianteInlineFormSet(instance=product, prefix="variants")
        
        # Prepara os dados de atributos para o JavaScript
        for form in variant_formset.forms:
            if form.instance.pk:
                # 🔴 CORREÇÃO: Usando o related_name 'variant_attributes' do seu model
                attrs = form.instance.variant_attributes.all() 
                attrs_data = [
                    {
                        "attribute_id": a.attribute.attribute_id, # Seu PK é attribute_id
                        "value": a.value
                    } 
                    for a in attrs
                ]
                form.initial_attributes_json = json.dumps(attrs_data)
            else:
                form.initial_attributes_json = "[]"

    elif request.method == 'POST':
        product_form = Product_Form(request.POST, request.FILES, instance=product, prefix="product")
        variant_formset = VarianteInlineFormSet(request.POST, request.FILES, instance=product, prefix="variants")
        
        deleted_variants_json = request.POST.get("deleted_variants")
        
        if product_form.is_valid() and variant_formset.is_valid():
            try:
                with transaction.atomic():
                    product = product_form.save()
                    
                    # Processa deleções de variantes enviadas pelo JS
                    if deleted_variants_json:
                        deleted_ids = json.loads(deleted_variants_json)
                        ProductVariant.objects.filter(product_variant_id__in=deleted_ids, product=product).delete()

                    # Salva as variantes (Formset)
                    variants = variant_formset.save()

                    # Processa os Atributos (VariantAttribute) via JSON
                    for i, form in enumerate(variant_formset.forms):
                        # Se o form foi marcado para deletar pelo formset padrão do Django
                        if form in variant_formset.deleted_forms:
                            continue
                            
                        variant = form.instance
                        if not variant.pk:
                            continue

                        # Pega o JSON de atributos específico desta variante (enviado pelo JS)
                        attr_json = request.POST.get(f"variants-{i}-attributes")
                        
                        if attr_json:
                            attributes_data = json.loads(attr_json)
                            
                            # 🔴 CORREÇÃO: Usando o related_name correto para limpar os antigos
                            variant.variant_attributes.all().delete() 
                            
                            for attr_item in attributes_data:
                                if attr_item.get("attribute_id") and attr_item.get("value"):
                                    # 🔴 CORREÇÃO: Nome do Model é VariantAttribute e FK é product_variant
                                    VariantAttribute.objects.create(
                                        product_variant=variant,
                                        attribute_id=attr_item["attribute_id"],
                                        value=attr_item["value"]
                                    )
                    
                    messages.success(request, "Produto atualizado com sucesso!")
                    return redirect("index")
            except Exception as e:
                messages.error(request, f"Erro ao salvar: {str(e)}")
        else:
            # Em caso de erro de validação, mantém os dados no template
            for i, form in enumerate(variant_formset.forms):
                form.initial_attributes_json = request.POST.get(f"variants-{i}-attributes", "[]")

    context = {
        "product_form": product_form,
        "variant_formset": variant_formset,
        "attribute_variant": Attributes_Form(), # Usado apenas para renderizar o template vazio
        "is_edit": True,
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
