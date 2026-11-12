"""
Roles del sistema - Integrante 5.

Se usan los Grupos de Django como roles:
  * Administrador : acceso total (habitaciones, usuarios, reportes).
  * Recepcionista : registra clientes y reservaciones; sólo consulta habitaciones.
"""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

GRUPO_ADMIN = "Administrador"
GRUPO_RECEPCION = "Recepcionista"

# Permisos de cada rol: (app, modelo, acciones)
PERMISOS_POR_ROL = {
    GRUPO_ADMIN: [
        ("habitaciones", "habitacion", ["view", "add", "change", "delete"]),
        ("clientes", "cliente", ["view", "add", "change", "delete"]),
        ("reservaciones", "reservacion", ["view", "add", "change", "delete"]),
    ],
    GRUPO_RECEPCION: [
        ("habitaciones", "habitacion", ["view"]),
        ("clientes", "cliente", ["view", "add", "change"]),
        ("reservaciones", "reservacion", ["view", "add", "change"]),
    ],
}


def es_administrador(user):
    """True para el superusuario o para quien pertenece al grupo Administrador."""
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name=GRUPO_ADMIN).exists()
    )


def nombre_rol(user):
    if user.is_superuser:
        return "Superusuario"
    grupo = user.groups.first()
    return grupo.name if grupo else "Sin rol"


class SoloAdministradorMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Para vistas que sólo puede ver un administrador (usuarios, reportes)."""

    def test_func(self):
        return es_administrador(self.request.user)

    def handle_no_permission(self):
        # Sin sesión -> login.  Con sesión pero sin rol de admin -> 403.
        if self.request.user.is_authenticated:
            raise PermissionDenied("Sólo un administrador puede entrar a esta sección.")
        return super().handle_no_permission()
