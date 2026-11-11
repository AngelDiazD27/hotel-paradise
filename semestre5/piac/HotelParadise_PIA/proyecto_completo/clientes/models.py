"""
Modelo Cliente - Integrante 2.

Regla 4: el correo del cliente debe ser único (unique=True + validación que
ignora mayúsculas/minúsculas en el formulario).
"""

from django.apps import apps
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

telefono_validator = RegexValidator(
    regex=r"^\d{10}$",
    message="El teléfono debe tener exactamente 10 dígitos (sin espacios ni guiones).",
)


class Cliente(models.Model):
    """Huésped del hotel."""

    nombre = models.CharField("nombre", max_length=80)
    apellidos = models.CharField("apellidos", max_length=120)
    correo = models.EmailField(
        "correo electrónico",
        unique=True,  # Regla 4
        error_messages={"unique": "Ya existe un cliente registrado con este correo."},
    )
    telefono = models.CharField("teléfono", max_length=10, validators=[telefono_validator])
    fecha_registro = models.DateTimeField("fecha de registro", auto_now_add=True)

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"
        ordering = ["apellidos", "nombre"]

    def __str__(self):
        return self.nombre_completo

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellidos}"

    def get_absolute_url(self):
        return reverse("clientes:detalle", args=[self.pk])

    def save(self, *args, **kwargs):
        # Normaliza el correo para que "Ana@Mail.com" y "ana@mail.com" sean el mismo.
        self.correo = self.correo.strip().lower()
        self.nombre = self.nombre.strip()
        self.apellidos = self.apellidos.strip()
        super().save(*args, **kwargs)

    def tiene_reservaciones_activas(self):
        """No se elimina un cliente que tiene una estancia pendiente o en curso."""
        if not apps.is_installed("reservaciones"):
            return False
        return self.reservaciones.filter(
            estado__in=["PENDIENTE", "CONFIRMADA"],
            fecha_salida__gte=timezone.localdate(),
        ).exists()
