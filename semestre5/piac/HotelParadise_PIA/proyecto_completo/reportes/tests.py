"""
Pruebas de reportes y estadísticas - Integrante 5.
Ejecutar:  python manage.py test reportes
"""

from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from clientes.models import Cliente
from habitaciones.models import Habitacion
from reservaciones.models import Reservacion

from . import estadisticas as est


class ReportesTests(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.create_superuser("admin", "a@a.com", "clave-segura-123"))
        c = Cliente.objects.create(nombre="Ana", apellidos="López", correo="ana@c.com", telefono="8112345678")
        h = Habitacion.objects.create(numero=1, tipo="SUITE", precio_noche=Decimal("1000"), capacidad=2)
        hoy = timezone.localdate()
        self.desde, self.hasta = date(hoy.year, 1, 1), date(hoy.year, 12, 31)
        base = max(hoy, date(hoy.year, 1, 1))
        Reservacion.objects.create(cliente=c, habitacion=h, fecha_entrada=base, fecha_salida=base + timedelta(days=2))
        Reservacion.objects.create(cliente=c, habitacion=h, fecha_entrada=base + timedelta(days=3),
                                   fecha_salida=base + timedelta(days=4), estado="CANCELADA")

    def test_ingresos_excluyen_canceladas(self):
        self.assertEqual(est.ingresos_totales(), Decimal("2000.00"))

    def test_resumen(self):
        r = est.resumen_general(self.desde, self.hasta)
        self.assertEqual(r["total_reservaciones"], 2)
        self.assertEqual(r["canceladas"], 1)

    def test_vista_reporte_y_csv(self):
        self.assertEqual(self.client.get(reverse("reportes:general")).status_code, 200)
        r = self.client.get(reverse("reportes:exportar_csv"))
        self.assertEqual(r["Content-Type"], "text/csv; charset=utf-8")
        self.assertIn("Folio", r.content.decode("utf-8-sig"))
