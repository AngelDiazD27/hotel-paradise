"""Filtro de periodo para los reportes - Integrante 5."""

from datetime import date

from django import forms
from django.utils import timezone

from core.forms import BootstrapFormMixin, FechaInput


def periodo_por_defecto():
    """Del 1 de enero al 31 de diciembre del año en curso."""
    hoy = timezone.localdate()
    return date(hoy.year, 1, 1), date(hoy.year, 12, 31)


class PeriodoForm(BootstrapFormMixin, forms.Form):
    desde = forms.DateField(label="Desde", widget=FechaInput())
    hasta = forms.DateField(label="Hasta", widget=FechaInput())

    def clean(self):
        datos = super().clean()
        if datos.get("desde") and datos.get("hasta") and datos["hasta"] < datos["desde"]:
            self.add_error("hasta", "La fecha final debe ser igual o posterior a la inicial.")
        return datos
