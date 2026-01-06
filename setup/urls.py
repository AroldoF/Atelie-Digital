from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

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


if settings.DEBUG:
    # Adiciona a rota para servir arquivos de mídia (MEDIA_URL) usando o caminho
    # definido em MEDIA_ROOT (no seu caso, BASE_DIR / 'media')
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # (servir arquivos estáticos no desenvolvimento local)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
