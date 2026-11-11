"""
Pruebas del módulo Reservaciones - Integrante 3.
Ejecutar:  python manage.py test reservaciones

Se prueban las Reglas 1, 2 y 5 (esta última desde la vista de habitaciones).
"""

from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from clientes.models import Cliente
from habitaciones.models import Habitacion

from .forms import ReservacionForm
from .models import Reservacion


class ReservacionTests(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.create_superuser("admin", "a@a.com", "clave-segura-123"))
        self.hoy = timezone.localdate()
        self.cliente = Cliente.objects.create(nombre="Ana", apellidos="López", correo="ana@c.com", telefono="8112345678")
        self.hab = Habitacion.objects.create(numero=101, tipo="DOBLE", precio_noche=Decimal("1000.00"), capacidad=2)
        self.reserva = Reservacion.objects.create(
            cliente=self.cliente, habitacion=self.hab,
            fecha_entrada=self.hoy + timedelta(days=5), fecha_salida=self.hoy + timedelta(days=8),
        )

    def form(self, entrada, salida, **extra):
        datos = {
            "cliente": self.cliente.pk, "habitacion": self.hab.pk,
            "fecha_entrada": (self.hoy + timedelta(days=entrada)).isoformat(),
            "fecha_salida": (self.hoy + timedelta(days=salida)).isoformat(),
            "num_huespedes": 1, "estado": "CONFIRMADA",
        }
        datos.update(extra)
        return ReservacionForm(data=datos)

    def test_total_se_calcula_solo(self):
        self.assertEqual(self.reserva.noches, 3)
        self.assertEqual(self.reserva.total, Decimal("3000.00"))

    def test_regla2_salida_mayor_que_entrada(self):
        f = self.form(10, 10)
        self.assertFalse(f.is_valid())
        self.assertIn("fecha_salida", f.errors)

    def test_regla1_no_se_traslapan(self):
        f = self.form(6, 9)  # choca con la reservación del día 5 al 8
        self.assertFalse(f.is_valid())
        self.assertIn("habitacion", f.errors)

    def test_salida_de_uno_es_entrada_del_siguiente(self):
        self.assertTrue(self.form(8, 10).is_valid())

    def test_cancelada_libera_la_habitacion(self):
        self.reserva.estado = Reservacion.Estado.CANCELADA
        self.reserva.save()
        self.assertTrue(self.form(6, 9).is_valid())

    def test_capacidad(self):
        f = self.form(20, 22, num_huespedes=5)
        self.assertFalse(f.is_valid())
        self.assertIn("num_huespedes", f.errors)

    def test_no_fechas_pasadas(self):
        self.assertFalse(self.form(-3, -1).is_valid())

    def test_cancelar_desde_la_vista(self):
        self.client.post(reverse("reservaciones:cancelar", args=[self.reserva.pk]))
        self.reserva.refresh_from_db()
        self.assertEqual(self.reserva.estado, Reservacion.Estado.CANCELADA)

    def test_disponibilidad_excluye_ocupadas(self):
        otra = Habitacion.objects.create(numero=102, tipo="DOBLE", precio_noche=900, capacidad=2)
        r = self.client.get(reverse("reservaciones:disponibilidad"), {
            "fecha_entrada": (self.hoy + timedelta(days=6)).isoformat(),
            "fecha_salida": (self.hoy + timedelta(days=7)).isoformat(),
            "huespedes": 1,
        })
        libres = list(r.context["libres"])
        self.assertIn(otra, libres)
        self.assertNotIn(self.hab, libres)

    def test_regla5_no_eliminar_habitacion_con_reservaciones_activas(self):
        self.client.post(reverse("habitaciones:eliminar", args=[self.hab.pk]))
        self.assertTrue(Habitacion.objects.filter(pk=self.hab.pk).exists())

    def test_crear_desde_la_vista(self):
        r = self.client.post(reverse("reservaciones:crear"), {
            "cliente": self.cliente.pk, "habitacion": self.hab.pk,
            "fecha_entrada": (self.hoy + timedelta(days=1)).isoformat(),
            "fecha_salida": (self.hoy + timedelta(days=3)).isoformat(),
            "num_huespedes": 2, "estado": "CONFIRMADA",
        })
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Reservacion.objects.count(), 2)
