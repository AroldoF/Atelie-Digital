from django.shortcuts import render
from .forms import FormLogin, FormRegisterUser, FormEditUser, FormAdressUser
# Create your views here.


def login(request):
    form = FormLogin(request.POST or None)
    return render(request, "accounts/login.html", {"form": form})

def register(request):
    form = FormRegisterUser(request.POST or None)
    return render(request, 'accounts/register.html', {'form': form})

def profile(request):
    return render(request, 'accounts/profile.html')

def settings(request):
    return render(request, "accounts/settings.html")

def settings_user(request):
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

def settings_address(request):
    form = FormAdressUser(request.POST or None)
    return render(request, 'accounts/settings_address.html', {'form': form})

def settings_artisian(request):
    return render(request, 'accounts/settings_artisian.html')

