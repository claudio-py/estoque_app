from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django import forms


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Digite seu usuário",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Digite sua senha",
            }
        ),
        label="Senha"
    )


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Digite nome de usuário"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Digite senha"}),
        label="Senha"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirme senha"}),
        label="Confirmar"
    )


    class Meta:
        model = User
        fields = ("username", "password1", "password2")
