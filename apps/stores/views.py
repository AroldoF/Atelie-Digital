from django.shortcuts import render
from django.views import View
from .forms import Store_Form, StoreCategories_Form

class Store_Register_View(View):
    def get(self, request):
        context = {
            'form': Store_Form(),
            'form_category': StoreCategories_Form()
        }
        return render(request, 'stores/register.html', context)
