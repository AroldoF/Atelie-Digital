from django import forms

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

class FormRegisterUser(forms.Form):
    name = forms.CharField(
        max_length=50, 
        label="Nome",
        widget=forms.TextInput(attrs={
            'placeholder': 'Maria José'
        })
    )
    cpf = forms.CharField(
        max_length=11, 
        label="CPF",
        widget=forms.TextInput(attrs={
            'placeholder': '00122099098'
        }),
        help_text= "Insira somente a numeração"
    )
    email = forms.EmailField(
        label="Email", 
        widget=forms.EmailInput(attrs={
            'placeholder': 'exemplo@gmail.com'
        })
    )    
    date = forms.DateField(
        label="Data de Nascimento",
        widget=forms.DateInput(attrs={
            'type':'date'
        })
    )
    cell_phone = forms.CharField(
        max_length=20, 
        label="Telefone",
        widget=forms.TextInput(attrs={
            'placeholder': '(DDD) 99999-9999'
        })
        )
    password = forms.CharField(
        label="Senha", 
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Crie uma senha segura'
        }), 
        help_text="Insira no mínimo 8 caracteres"
    )
    password_confirm = forms.CharField(
        label="Confirme a senha", 
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite a mesma senha'
        })
    )


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
    date = forms.DateField(
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
