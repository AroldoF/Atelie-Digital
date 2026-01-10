from django import forms
from django_cpf_cnpj.validators import validate_cnpj
from django.core.exceptions import ValidationError
import re

from .models import Store
 
class StoreCreationForm(forms.ModelForm):
    category_name = forms.CharField(
        label='Categoria Principal',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Ex: Tecidos, Cerâmica...',
            'list':'category_list', 
            'autocomplete': 'off'
        })
    )

    cnpj = forms.CharField(
        max_length=18,
        label='CNPJ',
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': '00.000.000/0000-00',
            'inputmode': 'numeric'
        }),
        help_text= "Insira somente a numeração"
    )

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
                'inputmode': 'numeric'
            }),
        }

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')

        if not cnpj:
            return None
    
        cnpj = re.sub(r'\D', '', cnpj)

        try:
            validate_cnpj(cnpj)
        except ValidationError:
            raise forms.ValidationError("CNPJ inválido")

        return cnpj
    
    def clean_phone_number(self):
        phone = re.sub(r'\D', '', self.cleaned_data['phone_number'])

        if len(phone) not in (10, 11):
            raise forms.ValidationError("Telefone inválido")

        return phone


    