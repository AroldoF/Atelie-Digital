from django.db import models
from django.db.models import Min, Sum, Value, OuterRef, Exists, Prefetch, BooleanField
from django.db.models.functions import Coalesce
from django.apps import apps

class ProductQuerySet(models.QuerySet):

    def active(self):
        return self.filter(is_active=True)

    def with_min_price(self):
        return self.annotate(
            min_price=Min('variants__price')
        )

    def with_total_sales(self):
        return self.annotate(
            total_sales=Coalesce(
                Sum('variants__order_products__quantity'),
                Value(0)
            )
        )

    def with_is_favorite(self, user):
        if not user.is_authenticated:
            return self.annotate(
                is_favorite=Value(False, output_field=BooleanField())
            )

        Favorite = apps.get_model('products', 'Favorite')

        favorite_subquery = Favorite.objects.filter(
            user_id=user,          
            product_id=OuterRef('pk') 
        )

        return self.annotate(
            is_favorite=Exists(favorite_subquery)
        )
    
    def with_sorted_variants(self):
        ProductVariant = apps.get_model('products', 'ProductVariant')

        return self.prefetch_related(
            Prefetch(
                'variants',
                queryset=ProductVariant.objects.order_by('price'),
                to_attr='sorted_variants'
            )
        )
    
    def cards(self):
        return (
            self.with_min_price()
            .with_sorted_variants()
        )
    
    def cards_with_favorites(self, user):
        return (
            self.with_min_price()
            .with_is_favorite(user)
            .with_sorted_variants()
        )

class ProductManager(models.Manager.from_queryset(ProductQuerySet)):
    def with_min_price(self):
        return self.get_queryset().with_min_price()

    def with_total_sales(self):
        return self.get_queryset().with_total_sales()

    def with_is_favorite(self, user):
        return self.get_queryset().with_is_favorite(user)

    def with_sorted_variants(self):
        return self.get_queryset().with_sorted_variants()

    def cards(self):
        return self.get_queryset().cards()

    def cards_with_favorites(self, user):
        return self.get_queryset().cards_with_favorites(user)