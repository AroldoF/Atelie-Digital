from django.shortcuts import render, redirect
from .forms import FormLogin, RegisterUserForm, FormEditUser, FormAdressUser,  AddressesForm
from django.views import View
from django.contrib import messages
# Create your views here.


def login(request):
    form = FormLogin(request.POST or None)
    return render(request, "accounts/login.html", {"form": form})

def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Error')
    else:
        form = RegisterUserForm()
    return render(request, 'accounts/register.html', {'form': form})

def profile(request):
    context = {'user': request.user}
    return render(request, 'accounts/profile.html', context)

def profileEdit(request):
    user = request.user

    if user.is_authenticated:
        form = FormEditUser(initial={
            'name': user.name,
            'email': user.email,
            'date': user.date,
            'cell_phone': user.cell_phone,
        })
    else:
        form = FormEditUser()
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