"""Formularios del módulo Habitaciones - Integrante 1."""

from django import forms

from core.forms import BootstrapFormMixin

from .models import Habitacion


class HabitacionForm(BootstrapFormMixin, forms.ModelForm):
    """Formulario para crear y editar habitaciones (CRUD)."""

    class Meta:
        model = Habitacion
        fields = [
            "numero",
            "tipo",
            "precio_noche",
            "capacidad",
            "disponible",
            "imagen",
            "descripcion",
        ]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
            "precio_noche": forms.NumberInput(attrs={"step": "0.01", "min": "1"}),
        }

    # Validaciones a nivel de campo: clean_<campo>()
    def clean_capacidad(self):
        capacidad = self.cleaned_data["capacidad"]
        if capacidad > 10:
            raise forms.ValidationError("La capacidad máxima permitida es de 10 personas.")
        return capacidad

    def clean_imagen(self):
        imagen = self.cleaned_data.get("imagen")
        # 2 MB como tamaño máximo para no llenar el disco del servidor.
        if imagen and hasattr(imagen, "size") and imagen.size > 2 * 1024 * 1024:
            raise forms.ValidationError("La imagen no debe pesar más de 2 MB.")
        return imagen


class BusquedaHabitacionForm(BootstrapFormMixin, forms.Form):
    """Filtros de la lista: búsqueda por número y por tipo de habitación."""

    q = forms.CharField(
        label="Buscar",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Número o descripción..."}),
    )
    tipo = forms.ChoiceField(
        label="Tipo",
        required=False,
        choices=[("", "Todos los tipos")] + Habitacion.TIPOS,
    )
    disponible = forms.ChoiceField(
        label="Estado",
        required=False,
        choices=[("", "Todas"), ("1", "Disponibles"), ("0", "Fuera de servicio")],
    )
