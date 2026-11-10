"""
Vistas de autenticación y control de usuarios - Integrante 5.

Login y Logout usan las vistas que ya trae Django (django.contrib.auth),
sólo se les cambia el template y el formulario.
"""

from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import LoginForm, UsuarioCrearForm, UsuarioEditarForm
from .permisos import SoloAdministradorMixin


class LoginView(auth_views.LoginView):
    template_name = "cuentas/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True  # Si ya inició sesión, lo manda al dashboard.

    def form_valid(self, form):
        messages.success(self.request, f"¡Bienvenido(a), {form.get_user().get_short_name() or form.get_user().username}!")
        return super().form_valid(form)


class LogoutView(auth_views.LogoutView):
    """Desde Django 5 el logout debe hacerse con POST (por seguridad)."""

    def post(self, request, *args, **kwargs):
        messages.info(request, "Cerraste sesión correctamente.")
        return super().post(request, *args, **kwargs)


class UsuarioListView(SoloAdministradorMixin, ListView):
    model = User
    template_name = "cuentas/usuarios_lista.html"
    context_object_name = "usuarios"

    def get_queryset(self):
        return User.objects.prefetch_related("groups").order_by("username")


class UsuarioCreateView(SoloAdministradorMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UsuarioCrearForm
    template_name = "cuentas/usuario_formulario.html"
    success_url = reverse_lazy("cuentas:usuarios")
    success_message = "Usuario %(username)s creado correctamente."


class UsuarioUpdateView(SoloAdministradorMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UsuarioEditarForm
    template_name = "cuentas/usuario_formulario.html"
    success_url = reverse_lazy("cuentas:usuarios")
    success_message = "Usuario actualizado correctamente."
    context_object_name = "usuario"

    def form_valid(self, form):
        # Evita que un administrador se desactive a sí mismo por error.
        if form.instance == self.request.user and not form.cleaned_data["is_active"]:
            form.add_error("is_active", "No puedes desactivar tu propia cuenta.")
            return self.form_invalid(form)
        return super().form_valid(form)
