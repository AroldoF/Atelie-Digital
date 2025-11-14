from django import forms

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
