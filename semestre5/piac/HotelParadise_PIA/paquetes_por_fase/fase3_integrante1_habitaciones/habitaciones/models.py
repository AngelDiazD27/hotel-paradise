"""
Modelo Habitacion - Integrante 1.

Reglas de negocio que se cumplen aquí:
  * Regla 3: no se pueden registrar habitaciones con números repetidos
    (unique=True en el campo `numero`).
  * Regla 5: no se puede eliminar una habitación con reservaciones activas
    (método `tiene_reservaciones_activas`, usado por la vista y el admin).
"""

from django.apps import apps
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Habitacion(models.Model):
    """Una habitación física del hotel."""

    # Tipos de habitación que maneja el hotel (choices = lista cerrada).
    INDIVIDUAL = "INDIVIDUAL"
    DOBLE = "DOBLE"
    SUITE = "SUITE"
    PRESIDENCIAL = "PRESIDENCIAL"
    TIPOS = [
        (INDIVIDUAL, "Individual"),
        (DOBLE, "Doble"),
        (SUITE, "Suite"),
        (PRESIDENCIAL, "Presidencial"),
    ]

    numero = models.PositiveIntegerField(
        "número",
        unique=True,  # Regla 3
        validators=[MinValueValidator(1)],
        error_messages={"unique": "Ya existe una habitación con este número."},
    )
    tipo = models.CharField("tipo", max_length=20, choices=TIPOS, default=INDIVIDUAL)
    precio_noche = models.DecimalField(
        "precio por noche",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)],
    )
    capacidad = models.PositiveSmallIntegerField(
        "capacidad (personas)", validators=[MinValueValidator(1)]
    )
    disponible = models.BooleanField(
        "disponible",
        default=True,
        help_text="Desmarca si la habitación está fuera de servicio (mantenimiento, limpieza profunda, etc.).",
    )
    imagen = models.ImageField("fotografía", upload_to="habitaciones/", blank=True, null=True)
    descripcion = models.TextField("descripción", blank=True)

    class Meta:
        verbose_name = "habitación"
        verbose_name_plural = "habitaciones"
        ordering = ["numero"]

    def __str__(self):
        return f"Hab. {self.numero} - {self.get_tipo_display()}"

    def get_absolute_url(self):
        return reverse("habitaciones:detalle", args=[self.pk])

    # --- Métodos de negocio -------------------------------------------------
    # `self.reservaciones` existe gracias al related_name="reservaciones" que
    # el Integrante 3 pone en Reservacion.habitacion. Mientras ese módulo no
    # esté instalado, estos métodos simplemente responden "no hay reservas".
    ESTADOS_ACTIVOS = ["PENDIENTE", "CONFIRMADA"]

    @staticmethod
    def _modulo_reservaciones_instalado():
        return apps.is_installed("reservaciones")

    def reservaciones_activas(self):
        """Reservaciones pendientes o confirmadas que todavía no terminan."""
        if not self._modulo_reservaciones_instalado():
            return []
        hoy = timezone.localdate()
        return self.reservaciones.filter(
            estado__in=self.ESTADOS_ACTIVOS, fecha_salida__gte=hoy
        )

    def tiene_reservaciones_activas(self):
        """Regla 5: True si la habitación NO se puede eliminar."""
        if not self._modulo_reservaciones_instalado():
            return False
        return self.reservaciones_activas().exists()

    def esta_ocupada_hoy(self):
        """True si hoy hay un huésped con reservación vigente."""
        if not self._modulo_reservaciones_instalado():
            return False
        hoy = timezone.localdate()
        return self.reservaciones.filter(
            estado__in=self.ESTADOS_ACTIVOS,
            fecha_entrada__lte=hoy,
            fecha_salida__gt=hoy,
        ).exists()
