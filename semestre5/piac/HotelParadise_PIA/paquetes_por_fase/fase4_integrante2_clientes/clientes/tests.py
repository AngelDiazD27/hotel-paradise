"""
Pruebas del módulo Clientes - Integrante 2.
Ejecutar:  python manage.py test clientes
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import ClienteForm
from .models import Cliente


class ClienteTests(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.create_superuser("admin", "a@a.com", "clave-segura-123"))
        self.ana = Cliente.objects.create(
            nombre="Ana", apellidos="López Garza", correo="ana@correo.com", telefono="8112345678"
        )

    def datos(self, **extra):
        base = {"nombre": "Luis", "apellidos": "Pérez", "correo": "luis@correo.com", "telefono": "8187654321"}
        base.update(extra)
        return base

    def test_crear_cliente(self):
        r = self.client.post(reverse("clientes:crear"), self.datos())
        self.assertEqual(r.status_code, 302)
        self.assertTrue(Cliente.objects.filter(correo="luis@correo.com").exists())

    def test_regla4_correo_unico_sin_importar_mayusculas(self):
        form = ClienteForm(data=self.datos(correo="ANA@Correo.com"))
        self.assertFalse(form.is_valid())
        self.assertIn("correo", form.errors)

    def test_correo_invalido(self):
        form = ClienteForm(data=self.datos(correo="no-es-correo"))
        self.assertFalse(form.is_valid())

    def test_telefono_10_digitos(self):
        self.assertFalse(ClienteForm(data=self.datos(telefono="81-12")).is_valid())

    def test_editar_conserva_su_propio_correo(self):
        form = ClienteForm(data=self.datos(correo="ana@correo.com", nombre="Ana María"), instance=self.ana)
        self.assertTrue(form.is_valid(), form.errors)

    def test_busqueda(self):
        Cliente.objects.create(nombre="Jorge", apellidos="Treviño", correo="jorge@correo.com", telefono="8100000000")
        r = self.client.get(reverse("clientes:lista"), {"q": "lópez"})
        self.assertContains(r, "López Garza")
        self.assertNotContains(r, "Treviño")

    def test_eliminar(self):
        self.client.post(reverse("clientes:eliminar", args=[self.ana.pk]))
        self.assertFalse(Cliente.objects.filter(pk=self.ana.pk).exists())
