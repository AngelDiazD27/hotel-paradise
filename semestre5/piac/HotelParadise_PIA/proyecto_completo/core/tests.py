"""
Pruebas del dashboard - Integrante 4.
Ejecutar:  python manage.py test core
"""

from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from clientes.models import Cliente
from habitaciones.models import Habitacion
from reservaciones.models import Reservacion


class DashboardTests(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.create_superuser("admin", "a@a.com", "clave-segura-123"))
        hoy = timezone.localdate()
        c = Cliente.objects.create(nombre="Ana", apellidos="López", correo="ana@c.com", telefono="8112345678")
        self.h1 = Habitacion.objects.create(numero=1, tipo="SUITE", precio_noche=Decimal("1000"), capacidad=2)
        Habitacion.objects.create(numero=2, tipo="DOBLE", precio_noche=Decimal("800"), capacidad=2)
        Habitacion.objects.create(numero=3, tipo="DOBLE", precio_noche=Decimal("800"), capacidad=2, disponible=False)
        Reservacion.objects.create(cliente=c, habitacion=self.h1, fecha_entrada=hoy, fecha_salida=hoy + timedelta(days=2))

    def test_indicadores(self):
        r = self.client.get(reverse("core:dashboard"))
        self.assertContains(r, "Ingresos generados")
        self.assertEqual(r.context["total_clientes"], 1)
        self.assertEqual(r.context["total_habitaciones"], 3)
        self.assertEqual(r.context["total_reservaciones"], 1)
        # 3 habitaciones: 1 ocupada hoy, 1 fuera de servicio -> 1 disponible
        self.assertEqual(r.context["habitaciones_disponibles"], 1)
        self.assertEqual(r.context["ingresos"], Decimal("2000.00"))

    def test_requiere_sesion(self):
        self.client.logout()
        self.assertEqual(self.client.get(reverse("core:dashboard")).status_code, 302)
