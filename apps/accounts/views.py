from django.shortcuts import render, redirect 
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .forms import LoginAuthenticationForm, RegisterUserForm, FormEditUser, FormAdressUser, AddressesForm
from .models import Profile 
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

    def get_success_url(self):
        return reverse_lazy('accounts:profile')

def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login_django(request, user)
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Erro ao cadastrar. Verifique os dados.")
    else:
        form = RegisterUserForm()
    
    return render(request, 'accounts/register.html', {'form': form})

# --- IMPLEMENTAÇÃO DA TASK MEU PERFIL ---

@never_cache
@login_required
def profile(request):
    template_name = 'accounts/profile.html'
    user = request.user

    # 1. Garantir que o Profile existe
    try:
        user_profile = user.profile
    except Exception:
        user_profile = Profile.objects.create(user=user)

    # 2. URL da Imagem Segura
    if user_profile.profile_image:
        profile_image_url = user_profile.profile_image.url
    else:
        profile_image_url = None 

    # 3. Buscar os 4 Últimos Pedidos
    last_orders = []
    if Order:
        last_orders = Order.objects.filter(user=user).order_by('-created_at')[:4]

    # 4. Buscar os 4 Últimos Favoritos
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

# --- OUTRAS VIEWS (Agora protegidas) ---

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
def usersOrders(request):
    # Futura view de listagem completa de pedidos
    pass
    
@login_required
def addressesList(request):
    return render(request, 'accounts/addresses.html', {'addresses': []})
    
# Adicionado LoginRequiredMixin para proteger a classe
class AddressesRegister(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'form': AddressesForm()
        }
        return render(request, 'accounts/address_register.html', context)
    
    def post(self, request):
        form = AddressesForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "Endereço cadastrado com sucesso!")
            return redirect('accounts:addresses')
        return render(request, 'accounts/address_register.html', {'form': form})

@login_required
def addressEdit(request, address_id):
    form = FormAdressUser(request.POST or None)
    return render(request, 'accounts/settings_address.html', {'form': form})

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
    # CAMINHO CORRIGIDO: aponta para o arquivo dentro do app 'orders'
    template_name = 'orders/list.html' 
    
    # Busca segura dos pedidos
    if Order:
        orders = Order.objects.filter(user=user).order_by('-created_at')
    else:
        orders = []

    # Lógica de Filtros
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