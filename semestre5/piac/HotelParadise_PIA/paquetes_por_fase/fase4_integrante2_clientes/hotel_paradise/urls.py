"""
Rutas principales del proyecto.

Cada app tiene su propio archivo urls.py y aquí sólo se "incluye" con un
prefijo. Así cada integrante trabaja en sus rutas sin pisar las de los demás.

Flujo de Django: Usuario -> URL -> Vista -> Formulario -> Modelo -> BD -> Template
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# Personalización del encabezado del Django Admin (Integrante 1)
admin.site.site_header = "Hotel Paradise - Administración"
admin.site.site_title = "Hotel Paradise"
admin.site.index_title = "Panel administrativo"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),                    # Integrante 4
    path("cuentas/", include("cuentas.urls")),         # Integrante 5
    path("habitaciones/", include("habitaciones.urls")),   # Integrante 1
    path("clientes/", include("clientes.urls")),       # Integrante 2
]

# En modo desarrollo Django sirve las fotos subidas (carpeta media/).
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
