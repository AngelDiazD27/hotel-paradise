"""
Dashboard principal - Integrante 4 (con las estadísticas del Integrante 5).

Muestra los 5 indicadores que pide el PIA:
  Total de Clientes · Total de Habitaciones · Total de Reservaciones
  Habitaciones Disponibles · Ingresos Generados
"""

from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.views.generic import TemplateView
from django.utils import timezone

from clientes.models import Cliente
from habitaciones.models import Habitacion
from reportes import estadisticas as est
from reservaciones.models import Reservacion


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        hoy = timezone.localdate()
        activas = Reservacion.objects.filter(estado__in=Reservacion.ESTADOS_ACTIVOS)

        # Habitaciones ocupadas HOY (hay un huésped dentro).
        ocupadas_hoy = activas.filter(
            fecha_entrada__lte=hoy, fecha_salida__gt=hoy
        ).values("habitacion_id")
        en_servicio = Habitacion.objects.filter(disponible=True)
        disponibles_hoy = en_servicio.exclude(pk__in=ocupadas_hoy)

        # Ingresos de los últimos 6 meses para la gráfica pequeña.
        inicio_6m = (hoy.replace(day=1) - timedelta(days=150)).replace(day=1)
        fin_mes = (hoy.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        por_mes = est.ingresos_por_mes(inicio_6m, fin_mes)

        # Ocupación por tipo de habitación (hoy)
        por_tipo = (
            Habitacion.objects.values("tipo")
            .annotate(
                total=Count("id"),
                ocupadas=Count("id", filter=Q(pk__in=ocupadas_hoy)),
            )
            .order_by("tipo")
        )
        nombres = dict(Habitacion.TIPOS)

        # Tablero de habitaciones: el estado de cada cuarto el día de hoy.
        ids_ocupadas = set(ocupadas_hoy.values_list("habitacion_id", flat=True))
        tablero = []
        for h in Habitacion.objects.order_by("numero"):
            if not h.disponible:
                estado = "fuera"
            elif h.pk in ids_ocupadas:
                estado = "ocupada"
            else:
                estado = "libre"
            tablero.append({"habitacion": h, "estado": estado})

        ctx.update(
            tablero=tablero,
            hoy=hoy,
            total_clientes=Cliente.objects.count(),
            total_habitaciones=Habitacion.objects.count(),
            total_reservaciones=Reservacion.objects.count(),
            habitaciones_disponibles=disponibles_hoy.count(),
            habitaciones_ocupadas=en_servicio.filter(pk__in=ocupadas_hoy).count(),
            fuera_servicio=Habitacion.objects.filter(disponible=False).count(),
            ingresos=est.ingresos_totales(),
            reservaciones_activas=activas.filter(fecha_salida__gte=hoy).count(),
            llegadas=activas.filter(fecha_entrada=hoy).select_related("cliente", "habitacion"),
            salidas=activas.filter(fecha_salida=hoy).select_related("cliente", "habitacion"),
            proximas=activas.filter(
                fecha_entrada__gt=hoy, fecha_entrada__lte=hoy + timedelta(days=7)
            ).select_related("cliente", "habitacion").order_by("fecha_entrada")[:6],
            ultimas=Reservacion.objects.select_related("cliente", "habitacion").order_by("-creada")[:5],
            ocupacion_tipo=[
                {
                    "tipo": nombres.get(f["tipo"], f["tipo"]),
                    "total": f["total"],
                    "ocupadas": f["ocupadas"],
                    "porcentaje": round(f["ocupadas"] * 100 / f["total"]) if f["total"] else 0,
                }
                for f in por_tipo
            ],
            grafica_ingresos={
                "etiquetas": [f["etiqueta"] for f in por_mes],
                "valores": [float(f["ingresos"]) for f in por_mes],
            },
        )
        return ctx
