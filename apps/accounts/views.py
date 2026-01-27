from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .forms import LoginAuthenticationForm, RegisterUserForm, FormEditUser, FormAdressUser, AddressesForm
from .models import Profile, Address
from django.views import View
from django.contrib import messages
from django.contrib.auth import login as login_django
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.core.paginator import Paginator
from apps.accounts.services import update_user_profile
from django.utils.http import url_has_allowed_host_and_scheme

from django.db import transaction
from django.db.models import Q 

# Importações dos Models para as queries
from apps.products.models import Product
try:
    from apps.orders.models import Order
except ImportError:
    Order = None

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginAuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, "Login realizado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "E-mail ou senha inválidos")
        return super().form_invalid(form)

def register(request):
    redirect_to = request.POST.get('next') or request.GET.get('next')

    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login_django(request, user)
            
            if next and url_has_allowed_host_and_scheme(url=redirect_to, allowed_hosts=request.get_host()):
                return redirect(redirect_to)
            
            return redirect('accounts:profile') 
    else:
        form = RegisterUserForm()

    context = {
        'form': form,
        'next': redirect_to
    }
    return render(request, 'accounts/register.html', context)


@never_cache
@login_required
def profile(request):
    template_name = 'accounts/profile.html'
    user = request.user

    try:
        user_profile = user.profile
    except Exception:
        user_profile = Profile.objects.create(user=user)

    if user_profile.profile_image:
        profile_image_url = user_profile.profile_image.url
    else:
        profile_image_url = None 

    last_orders = []
    if Order:
        last_orders = Order.objects.filter(user=user).order_by('-created_at')[:4]

    try:
        last_favorites = Product.objects.cards_with_favorites(user).filter(is_favorite=True).order_by('-product_id')[:4]
    except AttributeError:
        from apps.products.models import Favorite
        favorites_qs = Favorite.objects.filter(user=user).select_related('product').order_by('-favorite_id')[:4]
        last_favorites = [fav.product for fav in favorites_qs]

    context = {
        'user': user,
        'profile_image_url': profile_image_url,
        'last_orders': last_orders,
        'last_favorites': last_favorites
    }
    
    return render(request, template_name, context)


@login_required
def profileEdit(request):
    user = request.user

    if request.method == "POST":
        form = FormEditUser(request.POST,request.FILES,user=user)

        if form.is_valid():
            update_user_profile(user=user,data=form.cleaned_data)
            messages.success(request, "Dados validados com sucesso!")
            return redirect('accounts:profile_edit')
        else:
            messages.error(request, "Corrija os erros abaixo.")

    else:
        form = FormEditUser(initial={
            'name': user.name,
            'email': user.email,
            'date_of_birth': (
            user.date_of_birth.strftime('%Y-%m-%d')
            if user.date_of_birth else None
            ),
            'cell_phone': user.phone_number,
            'cpf': user.cpf,
        },
            user=user
        )
    
    return render(request, 'accounts/settings_user.html', {'form': form})

@login_required
def becomeArtisian(request):
    return render(request, 'accounts/settings_artisian.html')
    
@login_required
def addressesList(request):
    addresses = Address.objects.filter(user=request.user).order_by('-is_main', 'address_id')
    return render(request, 'accounts/addresses.html', {'addresses': addresses})
 
class AddressesRegister(LoginRequiredMixin, View):
    def get(self, request):
        next_url = request.GET.get('next', '')
        
        context = {
            'form': AddressesForm(),
            'next_url': next_url 
        }
        return render(request, 'accounts/address_register.html', context)
    
    def post(self, request):
        form = AddressesForm(request.POST)
        next_url = request.POST.get('next') or request.GET.get('next', '')

        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            
            if not Address.objects.filter(user=request.user).exists():
                address.is_main = True
                
            address.save()
            messages.success(request, "Endereço cadastrado com sucesso!")
            
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts=None):
                return redirect(next_url)
            
            return redirect('accounts:addresses')
            
        return render(request, 'accounts/address_register.html', {'form': form, 'next_url': next_url})

@login_required
def addressEdit(request, address_id):
    address = get_object_or_404(Address, pk=address_id, user=request.user)
    next_url = request.POST.get('next') or request.GET.get('next', '')

    if request.method == 'POST':
        form = AddressesForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "Endereço atualizado com sucesso!")
            
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts=None):
                return redirect(next_url)
                
            return redirect('accounts:addresses')
    else:
        form = AddressesForm(instance=address)
        
    return render(request, 'accounts/settings_address.html', {'form': form, 'next_url': next_url})
@login_required
def addressDelete(request, address_id):
    address = get_object_or_404(Address, pk=address_id, user=request.user)
    address.delete()
    
    remaining_addresses = Address.objects.filter(user=request.user)
    
    if remaining_addresses.count() == 1:
        single_address = remaining_addresses.first()
        if not single_address.is_main:
            single_address.is_main = True
            single_address.save()
            
    elif remaining_addresses.exists() and not remaining_addresses.filter(is_main=True).exists():
        new_main = remaining_addresses.first()
        new_main.is_main = True
        new_main.save()

    messages.success(request, "Endereço removido com sucesso!")
    return redirect('accounts:addresses')

@login_required
def favoriteProduct(request):
    user = request.user
    products = Product.objects.cards_with_favorites(user).filter(is_favorite=True)

    order = request.GET.get('sort')
    search = request.GET.get('q')

    if search:
        products = products.filter(Q(name__icontains=search) | Q(description__icontains=search))

    if order == 'recentes':
        products = products.order_by('-pk') 
    elif order == 'antigos':
        products = products.order_by('pk')
    elif order == 'preco_menor':
        products = products.order_by('min_price')
    elif order == 'preco_maior':
        products = products.order_by('-min_price')
    
    paginator = Paginator(products, 4)
    page_number = request.GET.get("page")
    products_page = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop('page', None)

    return render(request, 'products/favoriteProducts.html',
        {
            'products': products_page,
            'total': products.count(),
            'query_string': query_params.urlencode(),
            'search': search
        }
    )

@login_required
def usersOrders(request):
    user = request.user
    template_name = 'orders/list.html' 
    
    if Order:
        orders = Order.objects.filter(user=user).order_by('-created_at')
    else:
        orders = []

    status_filter = request.GET.get('status')
    active_filter = 'all'

    if status_filter:
        valid_statuses = ['PENDING', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED']
        if status_filter in valid_statuses:
            orders = orders.filter(status=status_filter)
            active_filter = status_filter

    orders_count = orders.count() if hasattr(orders, 'count') else len(orders)

    context = {
        'orders': orders,
        'active_filter': active_filter,
        'orders_count': orders_count
    }
    
    return render(request, template_name, context)

@login_required
def addressSetDefault(request, address_id):
    """
    Define um endereço específico como o padrão (is_main=True)
    e remove o status de padrão de todos os outros endereços do usuário.
    """
    address = get_object_or_404(Address, pk=address_id, user=request.user)
    
    with transaction.atomic():
        # 1. Desmarca 'is_main' de todos os endereços desse usuário
        Address.objects.filter(user=request.user).update(is_main=False)
        
        # 2. Marca o endereço selecionado como principal
        address.is_main = True
        address.save()
        
    messages.success(request, f"O endereço '{address.street}' foi definido como padrão.")
    return redirect('accounts:addresses')