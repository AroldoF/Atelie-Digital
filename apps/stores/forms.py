from django import forms
from django_cpf_cnpj.validators import validate_cnpj
from .models import Store, StoreCategory
 
class StoreCreationForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description', 'email', 'phone_number', 'cnpj', 'image', 'banner']
        labels = {
            'name': 'Nome', 
            'description': 'Descrição', 
            'email': 'Email', 
            'phone_number': "Telefone da loja", 
            'cnpj': 'CNPJ',
            'image': 'Imagem',
            'banner': 'Banner da Loja'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da Loja'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição da Loja'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'exemplo@email.com'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999',
                'inputmode': 'numeric',
                'id': 'phone_number'
            }),
            'cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00.000.000/0000-00',
                'inputmode': 'numeric',
                'id': 'cnpj'
            }),
        }


class StoreCategories_Form(forms.ModelForm):
    class Meta: 
        model = StoreCategory
        labels = {'category': 'Categorias da Loja'}
        fields = ['category']
        widgets = {
            'category': forms.TextInput(attrs={
                'placeholder': 'Digite as Categorias'
            })
        }

       
    