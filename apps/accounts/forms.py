from django import forms
from datetime import date
from .models import User, Address
from django.contrib.auth.forms import UserCreationForm
import re




BRAZILIAN_STATES = [
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
]


class FormLogin(forms.Form):
    email = forms.EmailField(
        label="Email", 
        widget=forms.EmailInput(attrs={
            'placeholder': 'exemplo@gmail.com'
        })
    )
    password = forms.CharField(
        label="Senha", 
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Insira sua senha'
        })
    )

class RegisterUserForm(UserCreationForm):
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Crie uma senha segura'
        }), 
    )
    password2 = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite a mesma senha'
        })
    )

    class Meta:
        model = User
        fields = ['name', 'email', 'cpf', 'phone_number', 'date_of_birth']
        labels = {
            'name': 'Nome',
            'email': 'E-mail',
            'cpf': 'CPF',
            'phone_number': 'Telefone',
            'date_of_birth':'Data de nascimento',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ex.: Maria José'
            }),
            'cpf': forms.TextInput(attrs={
                'placeholder': 'Ex.: 001.220.990-98'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Ex.: exemplo@gmail.com'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'type':'date'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Ex.: (DDD) 99999-9999'
            }),

         
        }
        help_texts = {
            'phone_number': 'Insire o DDD e o dígito 9',
            'cpf': 'Insira somente a numeração',
        }
    
    def clean_cpf(self):
        cpf = re.sub(r'\D', '', self.cleaned_data['cpf'])

        if len(cpf) != 11 or cpf == cpf[0] * 11:
            raise forms.ValidationError("CPF inválido")
        
    #  adicionar validação da verificação de digitos

        return cpf

    def clean_phone_number(self):
        phone = re.sub(r'\D', '', self.cleaned_data['phone_number'])

        if len(phone) not in (10, 11):
            raise forms.ValidationError("Telefone inválido")

        return phone

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']

        if dob and dob > date.today():
            raise forms.ValidationError("Data de nascimento inválida")

        return dob
    
    
    def save(self, commit=True):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']

        base_username = email.split('@')[0]
        username = base_username
        counter = 1

        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            name=self.cleaned_data['name'],
            cpf=self.cleaned_data['cpf'],
            phone_number=self.cleaned_data['phone_number'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            is_active=True,
        )

        return user


class FormEditUser(forms.Form):
    profile_image = forms.ImageField(
        label="Foto de Perfil",
        required=False, # False para não obrigar o usuário a trocar a foto toda vez
        widget=forms.FileInput(attrs={
            'accept': 'image/*' # Opcional: ajuda o navegador a filtrar apenas imagens
        })
    )
    cpf = forms.CharField(
        max_length=11, 
        label="CPF",
        widget=forms.TextInput(attrs={
            'placeholder': '00122099098',
            'disabled': 'disabled'
        }),
        help_text= "Insira somente a numeração"
    )
    name = forms.CharField(
        max_length=50,
        label="Nome",
        widget=forms.TextInput(attrs={
            'placeholder': 'Maria José'
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'placeholder': 'exemplo@gmail.com'
        })
    )
    date_of_birth = forms.DateField(
        label="Data de Nascimento",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    cell_phone = forms.CharField(
        max_length=20,
        label="Telefone",
        widget=forms.TextInput(attrs={
            'placeholder': '(DDD) 99999-9999'
        })
    )

class FormAdressUser(forms.Form):
    cep = forms.CharField(
        label="CEP",
        max_length=9, 
        required=False
    )
    address = forms.CharField(
        label="Endereço",
        max_length=100,
    )
    number = forms.IntegerField(
        label="Número"
    )
    complement = forms.CharField(
        label="Complemento",
        max_length=50
    )
    neighb = forms.CharField(
        label="Bairro",
        max_length=50
    )
    city = forms.CharField(
        label="Cidade",
        max_length=80
    )
    state = forms.MultipleChoiceField(
        choices=BRAZILIAN_STATES,
        label="Estado",
         widget=forms.Select(attrs={'class': 'form-select'})
    )
    
class AddressesForm(forms.ModelForm):
    class Meta: 
        model = Address
        fields = ['street', 'neighborhood', 'number','city', 'cep', 'state', 'complement']
        labels = {
            'street': 'Rua', 
            'neighborhood': 'Bairro', 
            'number': 'Número da Casa',
            'city': 'Cidade', 
            'cep': 'CEP', 
            'state': 'Estado', 
            'complement': 'Complemento'
        }
        widgets = {
            'street': forms.TextInput(attrs={
                'placeholder': 'Ex.: 15 de março'
            }), 
            'neighborhood': forms.TextInput(attrs={
                'placeholder': 'Ex: Centro'
            }), 
            'number': forms.NumberInput(attrs={
                'placeholder': 'Ex.: 254'
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'Ex.: Pau dos Ferros'
            }), 
            'cep': forms.TextInput(attrs={
                'placeholder': 'Ex.: 59900-000'
            }), 
            'state': forms.TextInput(attrs={
                'placeholder': 'Ex.: RN'
            }), 
            'complement': forms.Textarea(attrs={
                'placeholder': 'Digite um referêncial para sua casa',
                'rows': 3
            })
        }
