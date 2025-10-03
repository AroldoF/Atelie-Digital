from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("stores/", include("apps.stores.urls")),
    path("products/", include("apps.products.urls")),
    path("orders/", include("apps.orders.urls")),
    path("chats/", include("apps.chats.urls")),
    path("reviews/", include("apps.reviews.urls")),
    path("", include("apps.core.urls")),
    path("", include("apps.utils.urls")),
]
