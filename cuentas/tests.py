"""
Pruebas de login, logout y roles - Integrante 5.
Ejecutar:  python manage.py test cuentas
"""

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse


class CuentasTests(TestCase):
    def setUp(self):
        call_command("crear_roles", verbosity=0)
        self.user = User.objects.create_user("recepcion", password="Clave-Prueba-2026")
        from django.contrib.auth.models import Group
        self.user.groups.add(Group.objects.get(name="Recepcionista"))

    def test_login_correcto(self):
        r = self.client.post(reverse("cuentas:login"), {"username": "recepcion", "password": "Clave-Prueba-2026"})
        self.assertRedirects(r, reverse("core:dashboard"), fetch_redirect_response=False)

    def test_login_incorrecto(self):
        r = self.client.post(reverse("cuentas:login"), {"username": "recepcion", "password": "mala"})
        self.assertContains(r, "Usuario o contraseña incorrectos")

    def test_logout(self):
        self.client.force_login(self.user)
        r = self.client.post(reverse("cuentas:logout"))
        self.assertRedirects(r, reverse("cuentas:login"), fetch_redirect_response=False)
        self.assertNotIn("_auth_user_id", self.client.session)  # ya no hay sesión

    def test_recepcionista_no_puede_crear_habitaciones(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse("habitaciones:crear")).status_code, 403)
        self.assertEqual(self.client.get(reverse("habitaciones:lista")).status_code, 200)

    def test_recepcionista_no_ve_usuarios(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse("cuentas:usuarios")).status_code, 403)

    def test_admin_crea_usuario(self):
        admin = User.objects.create_superuser("admin", "a@a.com", "clave-segura-123")
        self.client.force_login(admin)
        r = self.client.post(reverse("cuentas:usuario_crear"), {
            "username": "nuevo", "first_name": "Nuevo", "last_name": "Usuario", "email": "",
            "password1": "Hotel-Paradise-99", "password2": "Hotel-Paradise-99", "rol": "Recepcionista",
        })
        self.assertEqual(r.status_code, 302)
        self.assertTrue(User.objects.get(username="nuevo").groups.filter(name="Recepcionista").exists())
