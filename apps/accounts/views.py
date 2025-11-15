from django.shortcuts import render
from .forms import FormLogin, FormRegisterUser
# Create your views here.


def login(request):
    form = FormLogin(request.POST or None)
    return render(request, "accounts/login.html", {"form": form})

def register(request):
    form = FormRegisterUser(request.POST or None)
    return render(request, 'accounts/register.html', {'form': form})

def profile(request):
    return render(request, 'accounts/profile.html')
