from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from apps.orders.models import Order
from .models import Store, StoreCategory
from .forms import StoreCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin

def is_artisian(user):
    return user.is_authenticated and user.groups.filter(name='Artisians').exists()

@method_decorator(never_cache, name='dispatch')
class StoreCreateView(LoginRequiredMixin, CreateView):
    model = Store
    form_class = StoreCreationForm
    template_name = 'stores/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = StoreCategory.objects.all().order_by('name')
        return context

    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, 'stores') and request.user.stores.exists():
            messages.info(request, "Você já possui uma loja cadastrada!")
            user_store = request.user.stores.first()
            return redirect('stores:dashboard', store_id=user_store.store_id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            with transaction.atomic():
                category_name = form.cleaned_data.get('category_name')
                if category_name:
                    category_obj, _ = StoreCategory.objects.get_or_create(
                        name=category_name.strip()
                    )
                    form.instance.category = category_obj

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
 

class StoreUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, store_id):
        store = get_object_or_404(Store, pk=store_id)

        return render(request, 'stores/register.html', context={
            'form': StoreCreationForm(instance=store),
            'categories': StoreCategory.objects.all().order_by('name')
        })

    def post(self, request, store_id):
        store = get_object_or_404(Store, pk=store_id)
        store_form = StoreCreationForm(request.POST, request.FILES, instance=store)

        if not store_form.is_valid():
            messages.error(request, 'Erro ao atualizar a loja. Tente novamente.')
            return render(request, 'stores/register.html', context={'form': store_form, 'categories': StoreCategory.objects.all().order_by('name')})
        
        category_name = store_form.cleaned_data.get('category_name')
        
        if category_name:
            category_obj, _ = StoreCategory.objects.get_or_create(
                name=category_name.strip()
            )
            store.category = category_obj

        store_form.save()

        messages.success(request, 'Loja atualizada com sucesso!')
        return redirect('stores:detail', store_id=store.store_id)
    
    def test_func(self):
        store = get_object_or_404(Store, pk=self.kwargs['store_id'])
        return self.request.user.groups.filter(name='Artisians').exists() and store.user == self.request.user
    
@never_cache
@user_passes_test(is_artisian)
def dashboard(request, store_id): 
    store = get_object_or_404(Store, pk=store_id)
    # Garante que o usuário só acesse o dashboard da SUA própria loja
    if store.user != request.user:
        return redirect('index') 
        
    return render(request, 'stores/dashboard.html', {'store': store, 'store_id': store_id})


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

    products = (
        store.products
        .with_min_price()
        .with_min_stock()
    )

    paginator = Paginator(products, 5)  
    page_number = request.GET.get("page")
    products_page = paginator.get_page(page_number)
    
    return render(
        request,
        'stores/artisan_products_table.html',
        {
            'store': store,
            'products_page': products_page,
            'products': products,
            'active_page': 'products',
        }
    )

@user_passes_test(is_artisian)
def artisan_orders(request, store_id):
    store = get_object_or_404(Store, pk=store_id, user=request.user)

    orders= (
        store.orders
        .select_related('user')
        .order_by('-created_at')
    )

    paginator = Paginator(orders, 5)  
    page_number = request.GET.get("page")
    orders_page = paginator.get_page(page_number)

    return render(request, 'stores/artisan_orders_table.html', {
            'store': store,
            'orders_page': orders_page,
            'active_page': 'orders',
        })

@login_required
@user_passes_test(is_artisian)
@transaction.atomic
def artisan_order_detail(request, store_id, order_id):
    # Garante que a loja pertence ao artesão logado
    store = get_object_or_404(Store, pk=store_id, user=request.user)
    # Busca o pedido garantindo que pertence à loja
    order = get_object_or_404(
        Order.objects.select_related('user').prefetch_related('items__product_variant__product'),
        pk=order_id,
        store=store
    )

  
    if request.method == 'POST':
        # Impedir alteração em pedidos cancelados ou concluídos
        if order.status in ['COMPLETED', 'CANCELLED']:
            messages.error(request, f"Não é possível alterar um pedido com status: {order.get_status_display()}.")
            return redirect('stores:artisan_order_detail', store_id=store.pk, order_id=order.pk)

        new_status = request.POST.get('status')
        valid_statuses = [choice[0] for choice in Order.ORDER_STATUS_CHOICES]

        if new_status in valid_statuses:
            order.status = new_status
            order.save()
            messages.success(request, f"Status do pedido #{order.order_code} atualizado com sucesso!")
        else:
            messages.error(request, "Status inválido selecionado.")
        
        return redirect('stores:artisan_order_detail', store_id=store.pk, order_id=order.pk)

  
    return render(
        request,
        'stores/artisan_order_detail.html',
        {
            'store': store,
            'order': order,
            'active_page': 'orders',
        }
    )