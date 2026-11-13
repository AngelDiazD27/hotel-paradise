"""
Comando: python manage.py cargar_demo [--reiniciar]      - Integrante 4

Llena la base de datos con información de ejemplo para la demostración y el
video: habitaciones con fotografía, clientes, reservaciones de todo el año y
dos usuarios (administrador y recepcionista).

  --reiniciar   borra habitaciones, clientes y reservaciones antes de cargar.
"""

import io
import random
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.core.files.base import ContentFile
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from clientes.models import Cliente
from cuentas.permisos import GRUPO_ADMIN, GRUPO_RECEPCION
from habitaciones.models import Habitacion
from reservaciones.models import Reservacion

HABITACIONES = [
    # numero, tipo, precio, capacidad, descripción
    (101, "INDIVIDUAL", "950.00", 1, "Cama matrimonial, escritorio y vista al jardín."),
    (102, "INDIVIDUAL", "950.00", 1, "Cama matrimonial y regadera de lluvia."),
    (103, "INDIVIDUAL", "990.00", 2, "Cama queen, ideal para viajes de negocios."),
    (104, "INDIVIDUAL", "990.00", 2, "Cama queen con balcón."),
    (201, "DOBLE", "1450.00", 4, "Dos camas matrimoniales y sala pequeña."),
    (202, "DOBLE", "1450.00", 4, "Dos camas matrimoniales con vista a la alberca."),
    (203, "DOBLE", "1550.00", 4, "Dos camas queen y balcón."),
    (204, "DOBLE", "1550.00", 4, "Dos camas queen, cerca del elevador."),
    (205, "DOBLE", "1450.00", 3, "Cama king y sofá cama."),
    (301, "SUITE", "2600.00", 4, "Recámara king, sala independiente y frigobar."),
    (302, "SUITE", "2600.00", 4, "Recámara king, jacuzzi y terraza."),
    (303, "SUITE", "2850.00", 5, "Suite familiar con dos recámaras."),
    (401, "PRESIDENCIAL", "5900.00", 6, "Piso completo: dos recámaras, comedor y terraza panorámica."),
    (402, "PRESIDENCIAL", "6400.00", 6, "Suite presidencial con alberca privada."),
]

NOMBRES = ["Ana", "Luis", "María", "Jorge", "Sofía", "Carlos", "Valeria", "Diego", "Fernanda",
           "Ricardo", "Daniela", "Alejandro", "Paola", "Miguel", "Andrea", "Javier", "Regina",
           "Emilio", "Camila", "Héctor", "Ximena", "Rodrigo"]
APELLIDOS = ["García López", "Martínez Ruiz", "Hernández Soto", "González Treviño", "Rodríguez Garza",
             "Pérez Villarreal", "Sánchez Cantú", "Ramírez Salinas", "Torres Elizondo", "Flores Leal",
             "Rivera Montemayor", "Gómez Guerra", "Díaz Cavazos", "Cruz Zambrano", "Morales Sada",
             "Reyes Garza", "Ortiz Lozano", "Castillo Benavides", "Vargas Tamez", "Mendoza Quiroga",
             "Silva Chapa", "Jiménez Rocha"]

COLORES_TIPO = {
    "INDIVIDUAL": ((38, 33, 95), (13, 143, 130)),
    "DOBLE": ((27, 24, 70), (67, 56, 202)),
    "SUITE": ((67, 56, 202), (185, 119, 14)),
    "PRESIDENCIAL": ((27, 24, 70), (194, 65, 75)),
}


def imagen_habitacion(numero, tipo):
    """Dibuja una ilustración sencilla de la habitación con Pillow."""
    from PIL import Image, ImageDraw

    ancho, alto = 800, 500
    c1, c2 = COLORES_TIPO[tipo]
    img = Image.new("RGB", (ancho, alto))
    d = ImageDraw.Draw(img)
    for y in range(alto):  # degradado vertical
        t = y / alto
        d.line([(0, y), (ancho, y)], fill=tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)))
    # ventana
    d.rounded_rectangle([520, 70, 730, 260], radius=10, fill=(214, 236, 245), outline=(255, 255, 255), width=8)
    d.line([(625, 70), (625, 260)], fill=(255, 255, 255), width=6)
    d.ellipse([650, 95, 700, 145], fill=(255, 214, 120))
    # piso
    d.rectangle([0, 390, ancho, alto], fill=(232, 226, 214))
    # cama(s)
    camas = {"INDIVIDUAL": 1, "DOBLE": 2, "SUITE": 1, "PRESIDENCIAL": 1}[tipo]
    ancho_cama = 300 if camas == 1 and tipo in ("SUITE", "PRESIDENCIAL") else 220
    x = 70
    for _ in range(camas):
        d.rounded_rectangle([x, 230, x + ancho_cama, 300], radius=12, fill=(250, 248, 243))  # cabecera
        d.rounded_rectangle([x - 10, 290, x + ancho_cama + 10, 400], radius=14, fill=(255, 255, 255))
        d.rounded_rectangle([x - 10, 330, x + ancho_cama + 10, 400], radius=14, fill=(c2[0], c2[1], c2[2]))
        d.rounded_rectangle([x + 20, 270, x + 95, 305], radius=10, fill=(236, 233, 225))
        d.rounded_rectangle([x + ancho_cama - 95, 270, x + ancho_cama - 20, 305], radius=10, fill=(236, 233, 225))
        x += ancho_cama + 50
    if tipo == "PRESIDENCIAL":  # candil
        d.line([(420, 0), (420, 60)], fill=(255, 230, 160), width=3)
        d.ellipse([395, 55, 445, 95], fill=(255, 230, 160))
    # placa con el número
    d.rounded_rectangle([30, 30, 200, 95], radius=10, fill=(255, 255, 255))
    try:
        from PIL import ImageFont
        fuente = ImageFont.load_default(size=40)
    except Exception:  # Pillow antiguo
        fuente = None
    d.text((115, 62), str(numero), fill=c1, anchor="mm", font=fuente)
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    return ContentFile(buffer.getvalue(), name=f"hab_{numero}.jpg")


class Command(BaseCommand):
    help = "Carga datos de ejemplo para la demostración del sistema."

    def add_arguments(self, parser):
        parser.add_argument("--reiniciar", action="store_true", help="Borra los datos antes de cargar.")

    @transaction.atomic
    def handle(self, *args, **options):
        random.seed(2026)
        if options["reiniciar"]:
            Reservacion.objects.all().delete()
            Cliente.objects.all().delete()
            Habitacion.objects.all().delete()
            self.stdout.write("Datos anteriores eliminados.")

        call_command("crear_roles", stdout=self.stdout)
        self._usuarios()
        habitaciones = self._habitaciones()
        clientes = self._clientes()
        n = self._reservaciones(habitaciones, clientes)
        self.stdout.write(self.style.SUCCESS(
            f"Listo: {len(habitaciones)} habitaciones, {len(clientes)} clientes y {n} reservaciones."
        ))
        self.stdout.write("Usuarios: admin / Paradise2026!   ·   recepcion / Recepcion2026!")

    def _usuarios(self):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@hotelparadise.mx", "Paradise2026!",
                                          first_name="Administrador", last_name="General")
        admin = User.objects.get(username="admin")
        admin.groups.set([Group.objects.get(name=GRUPO_ADMIN)])
        if not User.objects.filter(username="recepcion").exists():
            u = User.objects.create_user("recepcion", "recepcion@hotelparadise.mx", "Recepcion2026!",
                                         first_name="Laura", last_name="Treviño")
            u.groups.set([Group.objects.get(name=GRUPO_RECEPCION)])

    def _habitaciones(self):
        resultado = []
        for numero, tipo, precio, capacidad, desc in HABITACIONES:
            h, creada = Habitacion.objects.get_or_create(
                numero=numero,
                defaults=dict(tipo=tipo, precio_noche=Decimal(precio), capacidad=capacidad, descripcion=desc),
            )
            if creada or not h.imagen:
                h.imagen.save(f"hab_{numero}.jpg", imagen_habitacion(numero, tipo), save=True)
            resultado.append(h)
        # Una habitación en mantenimiento para que se vea en el tablero.
        for h in resultado:
            if h.numero == 205 and h.disponible:
                h.disponible = False
                h.save(update_fields=["disponible"])
        return resultado

    def _clientes(self):
        resultado = []
        hoy = timezone.now()
        for i, (nombre, apellidos) in enumerate(zip(NOMBRES, APELLIDOS)):
            usuario = f"{nombre}.{apellidos.split()[0]}".lower()
            for a, b in (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("ñ", "n")):
                usuario = usuario.replace(a, b)
            c, creado = Cliente.objects.get_or_create(
                correo=f"{usuario}@correo.com",
                defaults=dict(nombre=nombre, apellidos=apellidos, telefono=f"81{random.randint(10000000, 99999999)}"),
            )
            if creado:  # fechas de registro repartidas en el año
                Cliente.objects.filter(pk=c.pk).update(fecha_registro=hoy - timedelta(days=300 - i * 13))
            resultado.append(c)
        return resultado

    def _reservaciones(self, habitaciones, clientes):
        if Reservacion.objects.exists():
            return Reservacion.objects.count()
        hoy = timezone.localdate()
        inicio = date(hoy.year, 1, 3)
        fin = hoy + timedelta(days=40)
        creadas = 0
        for h in habitaciones:
            dia = inicio + timedelta(days=random.randint(0, 6))
            while dia < fin:
                noches = random.choice([1, 2, 2, 3, 3, 4, 5, 7])
                salida = dia + timedelta(days=noches)
                if salida < hoy:
                    estado = random.choices(
                        [Reservacion.Estado.FINALIZADA, Reservacion.Estado.CANCELADA], [9, 1]
                    )[0]
                elif dia <= hoy:
                    estado = Reservacion.Estado.CONFIRMADA
                else:
                    estado = random.choices(
                        [Reservacion.Estado.CONFIRMADA, Reservacion.Estado.PENDIENTE, Reservacion.Estado.CANCELADA],
                        [6, 3, 1],
                    )[0]
                if h.disponible or salida < hoy:
                    Reservacion.objects.create(
                        cliente=random.choice(clientes),
                        habitacion=h,
                        fecha_entrada=dia,
                        fecha_salida=salida,
                        num_huespedes=random.randint(1, h.capacidad),
                        estado=estado,
                    )
                    creadas += 1
                # hueco entre huéspedes: menos ocupación al inicio del año
                hueco = random.randint(0, 9) if dia.month < 6 else random.randint(0, 5)
                dia = salida + timedelta(days=hueco)
        # Al menos dos llegadas para hoy (para la demostración).
        for h in Habitacion.objects.filter(disponible=True).order_by("?")[:6]:
            if not Reservacion.reservaciones_que_chocan(h, hoy, hoy + timedelta(days=2)).exists():
                Reservacion.objects.create(cliente=random.choice(clientes), habitacion=h, fecha_entrada=hoy,
                                           fecha_salida=hoy + timedelta(days=2), estado=Reservacion.Estado.CONFIRMADA)
                creadas += 1
                if Reservacion.objects.filter(fecha_entrada=hoy).count() >= 2:
                    break
        return creadas
