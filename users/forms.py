from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UserChangeForm
from .models import User
from django import forms


# Formulário de login personalizado
class CustomLoginForm(AuthenticationForm):
    # Campo de nome de usuário com placeholder no input
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Digite seu usuário",
            }
        )
    )

    # Campo de senha com placeholder e mascaramento do input
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Digite sua senha",
            }
        ),
        label="Senha"
    )


# Formulário de registro de usuário baseado no UserCreationForm
class RegisterUserForm(UserCreationForm):
    # Campo de nome de usuário com placeholder
    image = forms.ImageField(required=False)

    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Digite nome de usuário"})
    )

    # Primeira senha com placeholder
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Digite senha"}),
        label="Senha"
    )

    # Confirmação da senha com placeholder
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirme senha"}),
        label="Confirmar"
    )

    class Meta:
        model = User                       # Modelo utilizado no formulário
        fields = ("username", "password1", "password2","image")  # Campos exibidos no form

class EditUserForm(UserChangeForm):
    password = None  # oculta campo password padrão do Django

    class Meta:
        model = User
        fields = ["username", "image"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Digite usuário"}),
        }

