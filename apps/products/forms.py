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
    image = forms.ImageField(
        label="Imagem",
        widget=forms.ClearableFileInput()
    )

class Product_Variant_Form(forms.Form): 
    TYPE_CHOICES = [
        ("DEMANDA", "Demanda"),
        ("ESTOQUE", "Estoque"),
    ]
    sku = forms.CharField(max_length=50, required=False)
    description = forms.CharField(
        label="Descrição",
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descreva o produto...'})
    )
    price = forms.DecimalField(
        label="Preço",
        min_value=0,
        decimal_places=2,
    )
    variant_type = forms.ChoiceField(
        label="Tipo", 
        choices=TYPE_CHOICES,
        widget=forms.RadioSelect()
    )
    stock = forms.IntegerField(
        label="Estoque", 
        required=False,
        widget= forms.IntegerField(attrs={'placeholder': 'Quantidade em Estoque..'})
    )
    production_days = forms.IntegerField(label="Dias de Produção", required=False)
    is_customizable = forms.BooleanField(label="Personalizável", required=False, initial=False)

    class Atributos_Variant_Form(forms.Form):
        atributo = forms.CharField(max_length=50, )
        value = forms.CharField(max_length=50)
