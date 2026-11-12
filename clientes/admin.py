"""Panel administrativo de Clientes - Integrante 2."""

from django.contrib import admin

from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellidos", "correo", "telefono", "fecha_registro")
    search_fields = ("nombre", "apellidos", "correo", "telefono")
    list_filter = ("fecha_registro",)
    date_hierarchy = "fecha_registro"
    ordering = ("apellidos", "nombre")
