"""Panel administrativo de Habitaciones - Integrante 1."""

from django.contrib import admin, messages
from django.utils.html import format_html

from .models import Habitacion


@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ("numero", "tipo", "precio_noche", "capacidad", "disponible", "miniatura")
    list_filter = ("tipo", "disponible")
    search_fields = ("numero", "descripcion")
    list_editable = ("precio_noche", "disponible")
    ordering = ("numero",)
    actions = ["marcar_disponibles", "marcar_fuera_de_servicio"]

    @admin.display(description="Foto")
    def miniatura(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="height:40px;border-radius:4px;">', obj.imagen.url
            )
        return "—"

    @admin.action(description="Marcar como disponibles")
    def marcar_disponibles(self, request, queryset):
        n = queryset.update(disponible=True)
        self.message_user(request, f"{n} habitación(es) marcadas como disponibles.")

    @admin.action(description="Marcar como fuera de servicio")
    def marcar_fuera_de_servicio(self, request, queryset):
        n = queryset.update(disponible=False)
        self.message_user(request, f"{n} habitación(es) fuera de servicio.")

    # --- Regla 5 también dentro del admin ----------------------------------
    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.tiene_reservaciones_activas():
            return False
        return super().has_delete_permission(request, obj)

    def delete_queryset(self, request, queryset):
        """Borrado masivo: omite las habitaciones con reservaciones activas."""
        bloqueadas = [h for h in queryset if h.tiene_reservaciones_activas()]
        if bloqueadas:
            numeros = ", ".join(str(h.numero) for h in bloqueadas)
            self.message_user(
                request,
                f"No se eliminaron las habitaciones {numeros} porque tienen reservaciones activas.",
                level=messages.WARNING,
            )
        queryset.exclude(pk__in=[h.pk for h in bloqueadas]).delete()
