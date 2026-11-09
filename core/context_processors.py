"""
Variables globales para los templates - Integrante 4.

`modulos` indica qué apps ya están instaladas. Así el menú de navegación
muestra cada sección en cuanto su integrante la agrega a INSTALLED_APPS,
sin romper el sitio mientras los demás módulos todavía no existen.
"""

from django.apps import apps

MODULOS = ["cuentas", "habitaciones", "clientes", "reservaciones", "reportes"]


def modulos_instalados(request):
    return {
        "modulos": {nombre: apps.is_installed(nombre) for nombre in MODULOS},
        "nombre_hotel": "Hotel Paradise",
    }
