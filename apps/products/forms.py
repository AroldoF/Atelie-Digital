from django import forms
from .models import ProductVariant, Product, VariantAttribute, VariantImage, ProductReview
from django.forms import inlineformset_factory, BaseInlineFormSet
from apps.utils.forms import is_empty_form, is_form_persisted

class ProductForm(forms.ModelForm):
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

class ProductVariantForm(forms.ModelForm): 
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
        cleaned_data = super().clean()
        variant_type = cleaned_data.get('type')
        
        if variant_type == 'STOCK':
            if not cleaned_data.get('stock'):
                self.add_error('stock', 'Este campo é obrigatório para produtos de estoque')
        elif variant_type == 'DEMAND':
            if not cleaned_data.get('production_days'):
                self.add_error('production_days', 'Este campo é obrigatório para produtos por demanda')
            # is_customizable não é obrigatório, mas pode ser validado conforme regra de negócio
        
        return cleaned_data

class AttributesForm(forms.ModelForm):
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
class VariantImageForm(forms.ModelForm):
    class Meta:
        model = VariantImage
        fields = ['image']

AttributeInlineFormSet = inlineformset_factory(
    ProductVariant,
    VariantAttribute,
    form=AttributesForm,
    min_num=1,
    validate_min=True,
    extra=0,
    can_delete=True
)

VariantImageInlineFormSet = inlineformset_factory(
    ProductVariant,
    VariantImage,
    form=VariantImageForm,
    min_num=1,
    validate_min=True,
    extra=0,
    can_delete=True
)

class Formset(BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)

        # Correção crítica: passa a instância correta para os formsets aninhados
        form.nested_images = VariantImageInlineFormSet(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix=f"{form.prefix}-images",
        )

        form.nested_attributes = AttributeInlineFormSet(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            prefix=f"{form.prefix}-attributes",
        )

        if self.can_delete and 'DELETE' in form.fields:
            form.fields['DELETE'].widget = forms.HiddenInput()

        if hasattr(form, "nested_images") and form.nested_images.can_delete:
            for img_form in form.nested_images.forms:
                if 'DELETE' in img_form.fields:
                    img_form.fields['DELETE'].widget = forms.HiddenInput()

        if hasattr(form, "nested_attributes") and form.nested_attributes.can_delete:
            for attr_form in form.nested_attributes.forms:
                if 'DELETE' in attr_form.fields:
                    attr_form.fields['DELETE'].widget = forms.HiddenInput()

    def clean(self):
        super().clean()
        
        skus = []
        
        for form in self.forms:
            if self._should_delete_form(form) or is_empty_form(form):
                continue

            # Validação de SKU (continua igual)
            sku = form.cleaned_data.get('sku')
            if sku:
                if sku in skus:
                    form.add_error('sku', "Este SKU já está sendo usado em outra variante.")
                skus.append(sku)

            # --- VALIDAÇÃO DE ATRIBUTOS (Versão Segura) ---
            if hasattr(form, "nested_attributes"):
                attributes_seen = []
                
                # Chamamos o full_clean do formset aninhado para garantir que o cleaned_data exista
                # Isso resolve o erro 'VariantAttributeForm' object has no attribute 'cleaned_data'
                form.nested_attributes.full_clean() 

                for attr_form in form.nested_attributes.forms:
                    # 1. Ignoramos se o form for vazio ou marcado para delete
                    if form.nested_attributes._should_delete_form(attr_form) or is_empty_form(attr_form):
                        continue
                    
                    # 2. Acessamos o cleaned_data com segurança
                    # Se o form tiver erros graves de campo, o cleaned_data pode não existir
                    data = getattr(attr_form, 'cleaned_data', None)
                    
                    if data:
                        attr_obj = data.get('attribute')
                        if attr_obj:
                            if attr_obj in attributes_seen:
                                attr_form.add_error('attribute', f"O atributo '{attr_obj}' já foi adicionado.")
                            else:
                                attributes_seen.append(attr_obj)

    def save(self, commit=True):
        for form in self.forms:
            delete = form.cleaned_data.get('DELETE', False)
            variant_attr_id = form.cleaned_data.get('variant_attributes_id')  # seu hidden field

            if delete and variant_attr_id:
                from .models import VariantAttribute
                try:
                    attr = VariantAttribute.objects.get(pk=variant_attr_id)
                    attr.delete()
                except VariantAttribute.DoesNotExist:
                    pass  # já deletado ou não existe
        result = super().save(commit=commit)
        
        for form in self.forms:
            if self._should_delete_form(form):
                continue
            if hasattr(form, "nested_attributes"):
                form.nested_attributes.save(commit=commit)
                
            if hasattr(form, "nested_images"):
                form.nested_images.save(commit=commit)

        return result


    def _is_adding_nested_inlines_to_empty_form(self, form):
        if is_form_persisted(form) or not is_empty_form(form):
            return False

        # Pega formulários não deletados de ambos os formsets
        attrs_active = set(form.nested_attributes.forms).difference(set(form.nested_attributes.deleted_forms))
        imgs_active = set(form.nested_images.forms).difference(set(form.nested_images.deleted_forms))

        # Se houver dados em QUALQUER um dos dois, mas a variante estiver vazia, retorna True (erro)
        attr_has_data = any(not is_empty_form(f) for f in attrs_active)
        img_has_data = any(not is_empty_form(f) for f in imgs_active)

        return attr_has_data or img_has_data
    
    def is_valid(self):
        result = super().is_valid()
        if self.is_bound:
            for form in self.forms:
                # Valida ambos os formsets aninhados
                if hasattr(form, "nested_attributes"):
                    result = result and form.nested_attributes.is_valid()
                if hasattr(form, "nested_images"):
                    result = result and form.nested_images.is_valid()
        return result
        


VarianteInlineFormSet = inlineformset_factory(
    Product,
    ProductVariant,
    form=ProductVariantForm,
    formset=Formset,
    min_num=1,
    validate_min=True,
    extra=0,
    can_delete=True
)

