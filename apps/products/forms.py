from django import forms
from crispy_forms.helper import FormHelper

class Product_Form(forms.Form):
    name = forms.CharField(
        label="Nome",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Digite o nome do produto'})
    )
    description = forms.CharField(
        label="Descrição",
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descreva o produto...'})
    )
    is_active = forms.BooleanField(
        label="Ativo",
        required=False,
    )

class Product_Variant_Form(forms.Form):
    # skull = 
    description = forms.CharField(
        label="Descrição",
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descreva o produto...'})
    )
    price = forms.DecimalField(
        label="Preço",
        min_value = 0,
        decimal_places=2,
    )