"""Panel administrativo de Reservaciones - Integrante 3."""

from django.contrib import admin

from .models import Reservacion


@admin.register(Reservacion)
class ReservacionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cliente",
        "habitacion",
        "fecha_entrada",
        "fecha_salida",
        "noches",
        "total",
        "estado",
    )
    list_filter = ("estado", "habitacion__tipo", "fecha_entrada")
    search_fields = (
        "cliente__nombre",
        "cliente__apellidos",
        "cliente__correo",
        "habitacion__numero",
    )
    date_hierarchy = "fecha_entrada"
    autocomplete_fields = ("cliente",)
    readonly_fields = ("total", "creada", "actualizada")
    list_select_related = ("cliente", "habitacion")
    actions = ["cancelar_seleccionadas"]

    @admin.display(description="Noches")
    def noches(self, obj):
        return obj.noches

    @admin.action(description="Cancelar reservaciones seleccionadas")
    def cancelar_seleccionadas(self, request, queryset):
        n = queryset.filter(estado__in=Reservacion.ESTADOS_ACTIVOS).update(
            estado=Reservacion.Estado.CANCELADA
        )
        self.message_user(request, f"{n} reservación(es) cancelada(s).")
