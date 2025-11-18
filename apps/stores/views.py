from django.shortcuts import render

# Create your views here.

def storeProfile(request):
    return render(request, 'stores/storeProfile.html')