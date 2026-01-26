from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic import TemplateView

from apps.core.views import (
    error_404_view,
    error_500_view,
    error_403_view,
    error_400_view
)

handler404 = error_404_view
handler500 = error_500_view
handler403 = error_403_view
handler400 = error_400_view

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


    # Teste com o debug = true para visualizar as páginas de erro
    path("teste-400/", TemplateView.as_view(template_name="errors/400.html")),
    path("teste-403/", TemplateView.as_view(template_name="errors/403.html")),
    path("teste-404/", TemplateView.as_view(template_name="errors/404.html")),
    path("teste-500/", TemplateView.as_view(template_name="errors/500.html")),
]


if settings.DEBUG:
    # Adiciona a rota para servir arquivos de mídia (MEDIA_URL) usando o caminho
    # definido em MEDIA_ROOT (no seu caso, BASE_DIR / 'media')
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # (servir arquivos estáticos no desenvolvimento local)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
