"""
Utilidades de formularios compartidas - Integrante 4.

`BootstrapFormMixin` agrega automáticamente las clases CSS de Bootstrap 5 a
todos los campos de un formulario, para que ningún integrante tenga que
escribir `attrs={"class": "form-control"}` en cada campo.
"""

from django import forms


class BootstrapFormMixin:
    """Mezcla (mixin) que se agrega a cualquier Form o ModelForm."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            widget = campo.widget
            if isinstance(widget, (forms.CheckboxInput,)):
                clase = "form-check-input"
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                clase = "form-select"
            else:
                clase = "form-control"
            clases_previas = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{clases_previas} {clase}".strip()

    def is_valid(self):
        """Marca en rojo (is-invalid) los campos que tienen errores."""
        valido = super().is_valid()
        for nombre in self.errors:
            if nombre in self.fields:
                w = self.fields[nombre].widget
                w.attrs["class"] = f"{w.attrs.get('class', '')} is-invalid".strip()
        return valido


class FechaInput(forms.DateInput):
    """Campo de fecha con el calendario nativo del navegador (type="date")."""

    input_type = "date"

    def __init__(self, attrs=None):
        super().__init__(attrs=attrs, format="%Y-%m-%d")
