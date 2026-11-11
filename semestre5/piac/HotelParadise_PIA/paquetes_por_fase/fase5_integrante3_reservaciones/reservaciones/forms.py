"""Formularios del módulo Reservaciones - Integrante 3."""

from django import forms

from clientes.models import Cliente
from core.forms import BootstrapFormMixin, FechaInput
from habitaciones.models import Habitacion

from .models import Reservacion


class ReservacionForm(BootstrapFormMixin, forms.ModelForm):
    """Registrar / modificar una reservación.

    Las Reglas 1 y 2 viven en Reservacion.clean(); un ModelForm las ejecuta
    automáticamente al llamar a form.is_valid().
    """

    class Meta:
        model = Reservacion
        fields = [
            "cliente",
            "habitacion",
            "fecha_entrada",
            "fecha_salida",
            "num_huespedes",
            "estado",
            "notas",
        ]
        widgets = {
            "fecha_entrada": FechaInput(),
            "fecha_salida": FechaInput(),
            "notas": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cliente"].queryset = Cliente.objects.order_by("apellidos", "nombre")
        habitaciones = Habitacion.objects.filter(disponible=True)
        if self.instance.pk:
            # Al editar se conserva la habitación actual aunque esté fuera de servicio.
            habitaciones = habitaciones | Habitacion.objects.filter(pk=self.instance.habitacion_id)
        else:
            # Una reservación nueva sólo puede nacer Pendiente o Confirmada.
            self.fields["estado"].choices = [
                (Reservacion.Estado.CONFIRMADA, "Confirmada"),
                (Reservacion.Estado.PENDIENTE, "Pendiente"),
            ]
        self.fields["habitacion"].queryset = habitaciones.distinct().order_by("numero")
        self.fields["habitacion"].label_from_instance = (
            lambda h: f"{h.numero} · {h.get_tipo_display()} · ${h.precio_noche:,.2f}/noche · {h.capacidad} pers."
        )
        # Datos para que el JavaScript calcule el total estimado en pantalla.
        self.precios = {str(h.pk): str(h.precio_noche) for h in self.fields["habitacion"].queryset}


class DisponibilidadForm(BootstrapFormMixin, forms.Form):
    """Consulta de disponibilidad por fechas, tipo y número de huéspedes."""

    fecha_entrada = forms.DateField(label="Fecha de entrada", widget=FechaInput())
    fecha_salida = forms.DateField(label="Fecha de salida", widget=FechaInput())
    tipo = forms.ChoiceField(
        label="Tipo de habitación",
        required=False,
        choices=[("", "Cualquier tipo")] + Habitacion.TIPOS,
    )
    huespedes = forms.IntegerField(label="Huéspedes", min_value=1, max_value=10, initial=1)

    def clean(self):
        datos = super().clean()
        entrada, salida = datos.get("fecha_entrada"), datos.get("fecha_salida")
        if entrada and salida and salida <= entrada:
            self.add_error("fecha_salida", "La fecha de salida debe ser mayor que la fecha de entrada.")
        return datos


class BusquedaReservacionForm(BootstrapFormMixin, forms.Form):
    cliente = forms.CharField(
        label="Cliente",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Nombre o correo"}),
    )
    habitacion = forms.IntegerField(
        label="Habitación",
        required=False,
        widget=forms.NumberInput(attrs={"placeholder": "Número"}),
    )
    tipo = forms.ChoiceField(
        label="Tipo",
        required=False,
        choices=[("", "Todos")] + Habitacion.TIPOS,
    )
    estado = forms.ChoiceField(
        label="Estado",
        required=False,
        choices=[("", "Todos")] + list(Reservacion.Estado.choices),
    )
