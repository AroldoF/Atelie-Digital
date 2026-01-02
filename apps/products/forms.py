from django import forms
from .models import ProductVariant, Product, VariantAttribute, ProductReview
from django.forms import inlineformset_factory

class Product_Form(forms.ModelForm):
    class Meta: 
        model = Product
        fields = ['name', 'description', 'image'] 
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
                'placeholder': 'Quantidade em Estoque',
                'display': "None"
            }),
            'production_days': forms.NumberInput(attrs={
                'placeholder': 'Quantidade em dias para produzir o produto'
            }),
            'is_customizable': forms.CheckboxInput(),
        }
        
    def clean(self):
        """Limpeza de múltiplos campos (lógica cruzada)"""
        cleaned_data = super().clean()
        v_type = cleaned_data.get('type')
        stock = cleaned_data.get('stock')
        production_days = cleaned_data.get('production_days')

        # Se for Sob Demanda, ignoramos o estoque e garantimos que seja 0 ou None
        if v_type == "Demand":
            cleaned_data['stock'] = 0 
            if not production_days:
                self.add_error('production_days', 'Para produtos sob demanda, informe os dias de produção.')

        # Se for Estoque, ignoramos dias de produção
        elif v_type == "Stock":
            cleaned_data['production_days'] = 0
            cleaned_data['is_customizable'] = False
            if stock is None:
                self.add_error('stock', 'Para produtos em estoque, informe a quantidade.')

        return cleaned_data

       
from django.forms.models import BaseInlineFormSet
from django.forms import HiddenInput

class HiddenDeleteInlineFormSet(BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)

        if self.can_delete and 'DELETE' in form.fields:
            form.fields['DELETE'].widget = HiddenInput()

VarianteInlineFormSet = inlineformset_factory(
    Product,
    ProductVariant,
    form=Product_Variant_Form,
    formset=HiddenDeleteInlineFormSet,
    extra=1,
    can_delete=True
)

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


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.HiddenInput(),
            "comment": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Escreva seu comentário..."
            })
        }
