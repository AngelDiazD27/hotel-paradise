"""
Pruebas del módulo Habitaciones - Integrante 1.
Ejecutar:  python manage.py test habitaciones
"""

from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import HabitacionForm
from .models import Habitacion


class HabitacionTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "a@a.com", "clave-segura-123")
        self.client.force_login(self.admin)
        self.hab = Habitacion.objects.create(
            numero=101, tipo=Habitacion.SUITE, precio_noche=Decimal("2500"), capacidad=3
        )

    def test_crear_habitacion_desde_la_vista(self):
        r = self.client.post(reverse("habitaciones:crear"), {
            "numero": 102, "tipo": "DOBLE", "precio_noche": "1500.00",
            "capacidad": 2, "disponible": "on", "descripcion": "",
        })
        self.assertEqual(r.status_code, 302)
        self.assertTrue(Habitacion.objects.filter(numero=102).exists())

    def test_regla3_numero_repetido(self):
        form = HabitacionForm(data={
            "numero": 101, "tipo": "DOBLE", "precio_noche": "1200", "capacidad": 2,
        })
        self.assertFalse(form.is_valid())
        self.assertIn("numero", form.errors)

    def test_capacidad_maxima(self):
        form = HabitacionForm(data={"numero": 500, "tipo": "SUITE", "precio_noche": "100", "capacidad": 20})
        self.assertFalse(form.is_valid())
        self.assertIn("capacidad", form.errors)

    def test_busqueda_por_tipo(self):
        Habitacion.objects.create(numero=201, tipo="DOBLE", precio_noche=1000, capacidad=2)
        r = self.client.get(reverse("habitaciones:lista"), {"tipo": "DOBLE"})
        self.assertContains(r, "Habitación 201")
        self.assertNotContains(r, "Habitación 101")

    def test_modificar_y_eliminar(self):
        r = self.client.post(reverse("habitaciones:editar", args=[self.hab.pk]), {
            "numero": 101, "tipo": "SUITE", "precio_noche": "2999.00", "capacidad": 3,
        })
        self.assertEqual(r.status_code, 302)
        self.hab.refresh_from_db()
        self.assertEqual(self.hab.precio_noche, Decimal("2999.00"))
        self.assertFalse(self.hab.disponible)  # el checkbox no se envió
        self.client.post(reverse("habitaciones:eliminar", args=[self.hab.pk]))
        self.assertFalse(Habitacion.objects.filter(pk=self.hab.pk).exists())

    def test_requiere_iniciar_sesion(self):
        self.client.logout()
        r = self.client.get(reverse("habitaciones:lista"))
        self.assertEqual(r.status_code, 302)
