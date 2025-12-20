from django.shortcuts import render
from django.views import View
from apps.products.models import Product, ProductVariant, Favorite
from django.db.models.functions import Coalesce
from django.db.models import Min, Sum, Value, Prefetch

class IndexView(View):
    def get(self, request):
        from django.db.models import Exists, OuterRef

        # usuário atual
        user = request.user

        favorite_subquery = Favorite.objects.filter(
            user=user,
            product=OuterRef('pk')
        )

        products = (
            Product.objects
            .annotate(
                min_price=Min('variants__price'),
                total_sales=Coalesce(
                    Sum('variants__order_products__quantity'),
                    Value(0)
                ),
                is_favorite=Exists(favorite_subquery)
            )
            .prefetch_related(
                Prefetch(
                    'variants',
                    queryset=ProductVariant.objects.order_by('price'),
                    to_attr='sorted_variants'
                )
            )
        )

        cheapest_products = (
            products
            .order_by('min_price')[:12]
        )

        best_selling_products = (
            products
            .order_by('-total_sales')[:12]
        )


        top_rated_products = (  #
            products
            .order_by('-pk')[:12]
        )

        context = {
            'cheapest_products': cheapest_products,
            'best_selling_products': best_selling_products,
            'top_rated_products': top_rated_products,
        }

        return render(request, "index.html", context)
