from django.shortcuts import render

# Create your views here.

def storeProfile(request):
    return render(request, 'stores/storeProfile.html')

def dashboard(request):
    return render(request, 'stores/dashboard.html')