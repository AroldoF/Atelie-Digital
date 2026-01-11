from django.shortcuts import render, redirect 
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .forms import LoginAuthenticationForm, RegisterUserForm, FormEditUser, FormAdressUser,  AddressesForm
from django.views import View
from django.contrib import messages
from django.contrib.auth import login as login_django
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.


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
            messages.success(request, "Seu cadastro foi realizado com sucesso!")
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Erro ao tentar realizar cadastro')
    else:
        form = RegisterUserForm()
    return render(request, 'accounts/register.html', {'form': form})

@never_cache
@login_required
def profile(request):
    context = {'user': request.user}
    return render(request, 'accounts/profile.html', context)


@never_cache
@login_required
def profileEdit(request):
    user = request.user

    if request.method == "POST":
        form = FormEditUser(request.POST,request.FILES,user=user)

        if form.is_valid():
            update_user_profile(user=user,data=form.cleaned_data)
            messages.success(request, "Dados validados com sucesso!")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Corrija os erros abaixo.")

    else:
        form = FormEditUser(initial={
            'name': user.name,
            'email': user.email,
            'date_of_birth': user.date_of_birth,
            'cell_phone': user.phone_number,
            'cpf': user.cpf,
        },
            user=user
        )
    
    return render(request, 'accounts/settings_user.html', {'form': form})

def settings(request):
    return render(request, "accounts/settings.html")

def becomeArtisian(request):
    return render(request, 'accounts/settings_artisian.html')

def addressesList(request):
    return render(request, 'accounts/addresses.html')

class AddressesRegister(View):
    def get(self, request):
        context = {
            'form': AddressesForm
        }
        return render(request, 'accounts/address_register.html', context)

def addressEdit(request):
    form = FormAdressUser(request.POST or None)
    return render(request, 'accounts/settings_address.html', {'form': form})

def favoriteProduct(request):
    return render(request, 'products/favoriteProducts.html')

def usersOrders(request):
    return render(request, "orders/list.html")