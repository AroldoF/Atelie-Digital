from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import user_passes_test

from .models import Store, StoreCategory
from .forms import StoreCreationForm

def is_artisian(user):
    return user.is_authenticated and user.groups.filter(name='Artisians').exists()

@method_decorator(never_cache, name='dispatch')
class StoreCreateView(LoginRequiredMixin, CreateView):
    model = Store
    form_class = StoreCreationForm
    template_name = 'stores/register.html' 

    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, 'stores') and request.user.stores.exists():
            messages.info(request, "Você já possui uma loja cadastrada!")
            user_store = request.user.stores.first()
            return redirect('stores:dashboard', store_id=user_store.store_id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            with transaction.atomic():
                form.instance.user = self.request.user
                self.object = form.save()
                
                from django.contrib.auth.models import Group
                group, _ = Group.objects.get_or_create(name='Artisians')
                self.request.user.groups.add(group)
                
                self.request.user.is_artisan = True
                self.request.user.save()
                
            messages.success(self.request, "Sua loja foi criada com sucesso!")
            return redirect(self.get_success_url())
            
        except Exception as e:
            messages.error(self.request, f"Erro ao processar o cadastro: {str(e)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Houve um erro no formulário. Verifique os dados e tente novamente.")
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse('stores:dashboard', kwargs={'store_id': self.object.store_id})
 

@never_cache
@user_passes_test(is_artisian)
def dashboard(request, store_id): 
    store = get_object_or_404(Store, pk=store_id)
    # Garante que o usuário só acesse o dashboard da SUA própria loja
    if store.user != request.user:
        return redirect('index') 
        
    return render(request, 'stores/dashboard.html', {'store': store, 'store_id': store_id})

@login_required
def store_detail(request, store_id):
    """
    Exibe a vitrine da loja.
    Acesso permitido a qualquer usuário logado (Clientes e Artesãos).
    """
    store = get_object_or_404(Store, pk=store_id, user__is_active=True)
    
    products = store.products.filter(is_active=True)

    context = {
        'store': store,
        'products': products
    }
    
    return render(request, 'stores/storeProfile.html', context)

@user_passes_test(is_artisian)
@login_required
@never_cache
def artisan_products(request, store_id):
    store = get_object_or_404(Store, pk=store_id, user=request.user)

    try:
        products = (
            store.products
            .with_min_price()
            .with_min_stock()
        )
    except AttributeError:
        products = store.products.all()

    return render(request, 'stores/products_list.html', {'store': store, 'products': products})

@user_passes_test(is_artisian)
def artisan_orders(request, store_id):
    store = get_object_or_404(Store, pk=store_id, user=request.user)
    orders= (
        store.orders
        .select_related('user')
        .order_by('-created_at')
    )
    return render(request, 'stores/artisan_orders_table.html', {
        'active_page': 'orders', 
        'store': store,
        'orders': orders,
        })

    

