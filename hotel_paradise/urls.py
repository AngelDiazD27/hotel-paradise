"""
Rutas principales del proyecto.

Cada app tiene su propio archivo urls.py y aquí sólo se "incluye" con un
prefijo. Así cada integrante trabaja en sus rutas sin pisar las de los demás.

Flujo de Django: Usuario -> URL -> Vista -> Formulario -> Modelo -> BD -> Template
"""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),                    # Integrante 4
        path("cuentas/", include("cuentas.urls")),      # Integrante 5

        path("habitaciones/", include("habitaciones.urls")),   # Integrante 1
        path("clientes/", include("clientes.urls")),       # Integrante 2
        path("reservaciones/", include("reservaciones.urls")), # Integrante 3
        path("reportes/", include("reportes.urls")),       # Integrante 5
    
    ]

