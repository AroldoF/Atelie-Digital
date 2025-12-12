from django import forms
from .models import ProductVariant, Product, VariantAttribute

class Product_Form(forms.ModelForm):
    class Meta: 
        model = Product
        fields = ['name', 'description', 'image'] #falta o campo de imagem
        labels = {
            'name': 'Nome',
            'description': 'Descrição'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Digite o nome do produto'
            }),
            'description': forms.Textarea (attrs={
                'rows': 4, 
                'placeholder': 'Descreva o produto'
            }),
            'image': forms.ClearableFileInput()
        }

class Product_Variant_Form(forms.ModelForm): 
    class Meta:
        model = ProductVariant
        exclude = ['product', 'is_active']
        labels = {
            'sku': 'Código da Variante',
            'description': 'Descrição',
            'price': 'Preço',
            'type': 'Tipo do Produto',
            'stock': 'Estoque',
            'production_days': 'Dias de Produção',
            'is_customizable': 'Personalizado',
        }
        widgets = {
            'sku': forms.TextInput(attrs={
                'placeholder': 'Código da Variante'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Descreva o produto'
            }), 
            'price': forms.NumberInput(attrs={
                'placeholder': 'Preço da variante'
            }),
            'type': forms.RadioSelect(),
            'stock': forms.NumberInput(attrs={
                'placeholder': 'Quantidade em Estoque'
            }),
            'production_days': forms.NumberInput(attrs={
                'placeholder': 'Quantidade em dias para produzir o produto'
            }),
            'is_customizable': forms.CheckboxInput(),
        }

class Attributes_Form(forms.ModelForm):
    class Meta:
        model = VariantAttribute
        exclude = ['product_variant']
        labels = {
            'attribute': 'Atributo',
            'value': 'Valor',
        }
        widgets = {
            'value': forms.TextInput (attrs={
                'placeholder': 'Digite o valor do atributo'
            })
        }