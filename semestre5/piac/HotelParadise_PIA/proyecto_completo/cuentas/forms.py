"""Formularios de login y control de usuarios - Integrante 5."""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group, User

from core.forms import BootstrapFormMixin

from .permisos import GRUPO_ADMIN, GRUPO_RECEPCION

ROLES = [(GRUPO_RECEPCION, "Recepcionista"), (GRUPO_ADMIN, "Administrador")]


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    error_messages = {
        "invalid_login": "Usuario o contraseña incorrectos. Verifica tus datos.",
        "inactive": "Esta cuenta está desactivada. Contacta al administrador.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"placeholder": "Usuario", "autofocus": True})
        self.fields["password"].widget.attrs.update({"placeholder": "Contraseña"})


def _asignar_rol(user, rol):
    grupo, _ = Group.objects.get_or_create(name=rol)
    user.groups.set([grupo])
    # Los administradores también pueden entrar al Django Admin.
    user.is_staff = rol == GRUPO_ADMIN
    user.save()


class UsuarioCrearForm(BootstrapFormMixin, UserCreationForm):
    first_name = forms.CharField(label="Nombre", max_length=150)
    last_name = forms.CharField(label="Apellidos", max_length=150)
    email = forms.EmailField(label="Correo", required=False)
    rol = forms.ChoiceField(label="Rol", choices=ROLES)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def save(self, commit=True):
        user = super().save(commit=True)
        _asignar_rol(user, self.cleaned_data["rol"])
        return user


class UsuarioEditarForm(BootstrapFormMixin, forms.ModelForm):
    rol = forms.ChoiceField(label="Rol", choices=ROLES)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "is_active")
        labels = {"is_active": "Cuenta activa"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        grupo = self.instance.groups.first()
        if grupo:
            self.fields["rol"].initial = grupo.name

    def save(self, commit=True):
        user = super().save(commit=True)
        _asignar_rol(user, self.cleaned_data["rol"])
        return user
