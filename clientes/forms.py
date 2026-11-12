"""Formularios del módulo Clientes - Integrante 2."""

from django import forms

from core.forms import BootstrapFormMixin

from .models import Cliente


class ClienteForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "apellidos", "correo", "telefono"]
        widgets = {
            "correo": forms.EmailInput(attrs={"placeholder": "nombre@correo.com"}),
            "telefono": forms.TextInput(
                attrs={"placeholder": "8112345678", "inputmode": "numeric", "maxlength": "10"}
            ),
        }

    def clean_correo(self):
        """Validación de correo (Regla 4) sin importar mayúsculas."""
        correo = self.cleaned_data["correo"].strip().lower()
        repetido = Cliente.objects.filter(correo__iexact=correo)
        if self.instance.pk:  # Al editar, se excluye al propio cliente.
            repetido = repetido.exclude(pk=self.instance.pk)
        if repetido.exists():
            raise forms.ValidationError("Ya existe un cliente registrado con este correo.")
        return correo

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()
        if any(c.isdigit() for c in nombre):
            raise forms.ValidationError("El nombre no debe contener números.")
        return nombre.title()

    def clean_apellidos(self):
        apellidos = self.cleaned_data["apellidos"].strip()
        if any(c.isdigit() for c in apellidos):
            raise forms.ValidationError("Los apellidos no deben contener números.")
        return apellidos.title()


class BusquedaClienteForm(BootstrapFormMixin, forms.Form):
    q = forms.CharField(
        label="Buscar",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Nombre, apellidos, correo o teléfono..."}),
    )
