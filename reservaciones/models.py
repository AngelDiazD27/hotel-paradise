"""
Modelo Reservacion - Integrante 3.

Relaciones (One-to-Many):
  Cliente    1 ---- N  Reservacion   (un cliente tiene muchas reservaciones)
  Habitacion 1 ---- N  Reservacion   (una habitación se reserva muchas veces)

Reglas de negocio que se validan aquí, en `clean()`:
  * Regla 1: una habitación no puede reservarse dos veces en las mismas fechas.
  * Regla 2: la fecha de salida debe ser mayor que la fecha de entrada.
  Además: capacidad de la habitación, habitación fuera de servicio y fechas
  pasadas al crear una reservación nueva.

La Regla 2 también se protege en la base de datos con un CheckConstraint.
"""

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Q
from django.urls import reverse
from django.utils import timezone

from clientes.models import Cliente
from habitaciones.models import Habitacion


class Reservacion(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        CONFIRMADA = "CONFIRMADA", "Confirmada"
        FINALIZADA = "FINALIZADA", "Finalizada"
        CANCELADA = "CANCELADA", "Cancelada"

    # Estados que "ocupan" la habitación en el calendario.
    ESTADOS_ACTIVOS = [Estado.PENDIENTE, Estado.CONFIRMADA]
    # Estados que cuentan como ingreso para el hotel (dashboard y reportes).
    ESTADOS_INGRESO = [Estado.CONFIRMADA, Estado.FINALIZADA]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="reservaciones",
        verbose_name="cliente",
    )
    habitacion = models.ForeignKey(
        Habitacion,
        on_delete=models.CASCADE,
        related_name="reservaciones",
        verbose_name="habitación",
    )
    fecha_entrada = models.DateField("fecha de entrada")
    fecha_salida = models.DateField("fecha de salida")
    num_huespedes = models.PositiveSmallIntegerField(
        "número de huéspedes", default=1, validators=[MinValueValidator(1)]
    )
    total = models.DecimalField(
        "total", max_digits=12, decimal_places=2, default=Decimal("0.00"), editable=False
    )
    estado = models.CharField(
        "estado", max_length=12, choices=Estado.choices, default=Estado.CONFIRMADA
    )
    notas = models.TextField("notas", blank=True)
    creada = models.DateTimeField("creada", auto_now_add=True)
    actualizada = models.DateTimeField("actualizada", auto_now=True)

    class Meta:
        verbose_name = "reservación"
        verbose_name_plural = "reservaciones"
        ordering = ["-fecha_entrada", "-id"]
        constraints = [
            # Regla 2 a nivel base de datos.
            models.CheckConstraint(
                condition=Q(fecha_salida__gt=F("fecha_entrada")),
                name="salida_mayor_que_entrada",
            )
        ]

    def __str__(self):
        return f"#{self.pk} {self.cliente} - Hab. {self.habitacion.numero}"

    def get_absolute_url(self):
        return reverse("reservaciones:detalle", args=[self.pk])

    # --- Cálculos -----------------------------------------------------------
    @property
    def noches(self):
        if self.fecha_entrada and self.fecha_salida:
            return (self.fecha_salida - self.fecha_entrada).days
        return 0

    def calcular_total(self):
        return self.habitacion.precio_noche * self.noches

    @property
    def es_activa(self):
        return self.estado in self.ESTADOS_ACTIVOS

    @property
    def puede_cancelarse(self):
        return self.estado in self.ESTADOS_ACTIVOS

    # --- Validaciones -------------------------------------------------------
    @classmethod
    def reservaciones_que_chocan(cls, habitacion, entrada, salida, excluir_pk=None):
        """Reservaciones activas de la habitación que se traslapan con el rango.

        Dos rangos [entrada, salida) se traslapan si:
            entrada_existente < salida_nueva  Y  salida_existente > entrada_nueva
        El día de salida de un huésped puede ser el día de entrada del siguiente.
        """
        qs = cls.objects.filter(
            habitacion=habitacion,
            estado__in=cls.ESTADOS_ACTIVOS,
            fecha_entrada__lt=salida,
            fecha_salida__gt=entrada,
        )
        if excluir_pk:
            qs = qs.exclude(pk=excluir_pk)
        return qs

    def clean(self):
        errores = {}
        entrada, salida = self.fecha_entrada, self.fecha_salida

        # Regla 2: salida > entrada
        if entrada and salida and salida <= entrada:
            errores["fecha_salida"] = "La fecha de salida debe ser mayor que la fecha de entrada."

        # Al crear (o reactivar) no se permiten fechas pasadas.
        if entrada and not self.pk and entrada < timezone.localdate():
            errores["fecha_entrada"] = "La fecha de entrada no puede ser anterior a hoy."

        habitacion = self.habitacion if self.habitacion_id else None
        if habitacion and self.es_activa:
            if not habitacion.disponible:
                errores["habitacion"] = (
                    f"La habitación {habitacion.numero} está fuera de servicio."
                )
            if self.num_huespedes and self.num_huespedes > habitacion.capacidad:
                errores["num_huespedes"] = (
                    f"La habitación {habitacion.numero} admite máximo "
                    f"{habitacion.capacidad} huésped(es)."
                )
            # Regla 1: disponibilidad (sin traslapes)
            if entrada and salida and salida > entrada:
                choques = self.reservaciones_que_chocan(habitacion, entrada, salida, self.pk)
                if choques.exists():
                    c = choques.first()
                    errores.setdefault(
                        "habitacion",
                        f"La habitación {habitacion.numero} ya está reservada del "
                        f"{c.fecha_entrada:%d/%m/%Y} al {c.fecha_salida:%d/%m/%Y}. "
                        "Elige otras fechas u otra habitación.",
                    )
        if errores:
            raise ValidationError(errores)

    def save(self, *args, **kwargs):
        # El total siempre lo calcula el sistema: noches x precio por noche.
        self.total = self.calcular_total()
        super().save(*args, **kwargs)
