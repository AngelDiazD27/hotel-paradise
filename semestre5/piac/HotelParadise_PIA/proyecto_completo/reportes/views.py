"""Reportes y estadísticas (sólo administradores) - Integrante 5."""

import csv

from django.http import HttpResponse
from django.views.generic import TemplateView

from cuentas.permisos import SoloAdministradorMixin

from . import estadisticas as est
from .forms import PeriodoForm, periodo_por_defecto


class PeriodoMixin:
    """Lee ?desde=...&hasta=... de la URL; si no vienen, usa el año actual."""

    def obtener_periodo(self):
        desde, hasta = periodo_por_defecto()
        datos = self.request.GET or {"desde": desde, "hasta": hasta}
        form = PeriodoForm(datos)
        if form.is_valid():
            desde, hasta = form.cleaned_data["desde"], form.cleaned_data["hasta"]
        return form, desde, hasta


class ReporteView(SoloAdministradorMixin, PeriodoMixin, TemplateView):
    template_name = "reportes/reporte.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form, desde, hasta = self.obtener_periodo()
        por_mes = est.ingresos_por_mes(desde, hasta)
        por_tipo = est.ingresos_por_tipo(desde, hasta)
        ocupacion, tasa = est.ocupacion_por_habitacion(desde, hasta)
        resumen = est.resumen_general(desde, hasta)
        ctx.update(
            form=form,
            desde=desde,
            hasta=hasta,
            resumen=resumen,
            por_mes=por_mes,
            por_tipo=por_tipo,
            mejores_clientes=est.mejores_clientes(desde, hasta),
            ocupacion=ocupacion,
            tasa_ocupacion=tasa,
            querystring=self.request.GET.urlencode(),
            # Datos para Chart.js (se pasan como JSON seguro con json_script)
            grafica_mes={
                "etiquetas": [f["etiqueta"] for f in por_mes],
                "valores": [float(f["ingresos"]) for f in por_mes],
            },
            grafica_tipo={
                "etiquetas": [f["tipo"] for f in por_tipo],
                "valores": [float(f["ingresos"]) for f in por_tipo],
            },
            grafica_estado={
                "etiquetas": [f["estado"] for f in resumen["por_estado"]],
                "valores": [f["n"] for f in resumen["por_estado"]],
            },
        )
        return ctx


class ExportarCSVView(SoloAdministradorMixin, PeriodoMixin, TemplateView):
    """Descarga las reservaciones del periodo en un archivo CSV (abre en Excel)."""

    def get(self, request, *args, **kwargs):
        _, desde, hasta = self.obtener_periodo()
        respuesta = HttpResponse(content_type="text/csv; charset=utf-8")
        respuesta["Content-Disposition"] = (
            f'attachment; filename="reservaciones_{desde:%Y%m%d}_{hasta:%Y%m%d}.csv"'
        )
        respuesta.write("﻿")  # BOM: para que Excel respete los acentos
        escritor = csv.writer(respuesta)
        escritor.writerow(
            ["Folio", "Cliente", "Correo", "Habitación", "Tipo", "Entrada", "Salida",
             "Noches", "Huéspedes", "Total", "Estado"]
        )
        qs = est.reservaciones_del_periodo(desde, hasta).select_related("cliente", "habitacion")
        for r in qs.order_by("fecha_entrada"):
            escritor.writerow([
                r.pk, r.cliente.nombre_completo, r.cliente.correo, r.habitacion.numero,
                r.habitacion.get_tipo_display(), r.fecha_entrada.isoformat(),
                r.fecha_salida.isoformat(), r.noches, r.num_huespedes, f"{r.total:.2f}",
                r.get_estado_display(),
            ])
        return respuesta
