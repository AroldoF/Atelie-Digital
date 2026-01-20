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
        # Valida se o usuário já possui uma loja (já é artesão)
        if hasattr(request.user, 'stores') and request.user.stores.exists():
            messages.info(request, "Você já possui uma loja cadastrada!")
            user_store = request.user.stores.first()
            return redirect('stores:dashboard', store_id=user_store.store_id)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Busca todas as categorias cadastradas para o datalist
        context['categories'] = StoreCategory.objects.all()
        return context

    def form_valid(self, form):
        try:
            with transaction.atomic():
                # 1. Associa o usuário logado à loja antes de salvar
                self.object = form.save(commit=False)
                self.object.user = self.request.user
                
                # 2. Lógica para Categoria (pegando do campo de texto do template)
                category_name = form.cleaned_data.get('category_name').strip().title()

                if category_name:
                    category_obj, created = StoreCategory.objects.get_or_create(name=category_name)
                    self.object.category = category_obj

                self.object.save()

                # 3. Implementar lógica para alterar que o usuário seja também um artesão
                user = self.request.user
                if not user.is_artisan:
                    user.is_artisan = True  
                    user.save()

                messages.success(self.request, "Sua loja foi cadastrada com sucesso! Agora você é um artesão.")
                return super().form_valid(form)
                
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
    return render(request, 'stores/dashboard.html', {'store': store, 'store_id': store_id})

@user_passes_test(is_artisian)
def storeProfile(request):
    return render(request, 'stores/storeProfile.html')

@user_passes_test(is_artisian)
@login_required
@never_cache
def artisan_products(request, store_id):
    store = get_object_or_404(Store, pk=store_id)

    return render(
        request,
        'stores/artisan_products_table.html',
        {
            'store': store,
            'store_id': store_id,
            'active_page': 'products'
        }
    )


@user_passes_test(is_artisian)
def artisan_orders(request):
    return render(request, 'stores/artisan_orders_table.html', {'active_page': 'orders'})

    

