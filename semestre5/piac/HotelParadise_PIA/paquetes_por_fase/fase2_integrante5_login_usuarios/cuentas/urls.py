"""Rutas de cuentas - Integrante 5."""

from django.urls import path

from . import views

app_name = "cuentas"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("usuarios/", views.UsuarioListView.as_view(), name="usuarios"),
    path("usuarios/nuevo/", views.UsuarioCreateView.as_view(), name="usuario_crear"),
    path("usuarios/<int:pk>/editar/", views.UsuarioUpdateView.as_view(), name="usuario_editar"),
]
