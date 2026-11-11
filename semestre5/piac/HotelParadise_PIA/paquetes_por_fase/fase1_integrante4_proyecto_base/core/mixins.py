"""
Mixins de acceso compartidos - Integrante 4.

`PermisoRequeridoMixin` junta dos comportamientos:
  * Si el usuario NO ha iniciado sesión -> lo manda a la pantalla de login.
  * Si ya inició sesión pero su rol no tiene el permiso -> página 403.

(Con LoginRequiredMixin + PermissionRequiredMixin y raise_exception=True,
Django mostraría 403 incluso a quien no ha iniciado sesión.)
"""

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied


class PermisoRequeridoMixin(LoginRequiredMixin, PermissionRequiredMixin):
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("Tu rol no tiene permiso para esta acción.")
        return super().handle_no_permission()
