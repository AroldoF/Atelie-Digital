from django.shortcuts import render
from django.views import View
from apps.products.models import Product

class IndexView(View):
    def get(self, request):
        # usuário atual
        user = request.user

        # Queryset base com todos os produtos
        products = Product.objects.cards_with_favorites(user)

        # Selecionando os 12 mais baratos
        cheapest_products = products.order_by('min_price')[:12]

        # Selecionando os 12 mais vendidos
        best_selling_products = products.with_total_sales().order_by('-total_sales')[:12]

        # Selecionando os 12 produtos "top rated" (mais recentes ou outro critério)
        top_rated_products = products.order_by('-pk')[:12]

        context = {
            'cheapest_products': cheapest_products,
            'best_selling_products': best_selling_products,
            'top_rated_products': top_rated_products,
        }

        return render(request, "index.html", context)
