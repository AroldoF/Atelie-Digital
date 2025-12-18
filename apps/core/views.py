from django.shortcuts import render
from django.views import View
from apps.products.models import Product, ProductVariant
from django.db.models import Min, Sum, Prefetch

class IndexView(View):
    def get(self, request):

        products = (
            Product.objects
            .annotate(min_price=Min('variants__price'))
            .prefetch_related(
                Prefetch(
                    'variants',
                    queryset=ProductVariant.objects.order_by('price'),
                    to_attr='sorted_variants'
                )
            )
        )

        cheapest_products = (  # produtos mais baratos
            products
            .annotate(min_price=Min('variants__price'))
            .order_by('min_price')[:12]
        )

        best_selling_products = (
            products
            .annotate(total_sales=Sum('variants__order_products__quantity'))  
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
