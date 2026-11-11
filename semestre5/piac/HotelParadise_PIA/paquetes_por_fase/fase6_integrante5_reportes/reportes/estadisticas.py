"""
Consultas avanzadas con el ORM de Django - Integrante 5.

Aquí se concentran las estadísticas para que el Dashboard (Integrante 4) y
los Reportes usen exactamente los mismos cálculos.

Conceptos que se practican:
  aggregate()  -> un solo resultado (SUMA total, CONTEO total)
  annotate()   -> un resultado por grupo (GROUP BY)
  values()     -> elegir las columnas por las que se agrupa
  TruncMonth   -> agrupar fechas por mes
  Coalesce     -> convertir NULL en 0
"""

from datetime import timedelta
from decimal import Decimal

from django.db.models import Count, DecimalField, Sum, Value
from django.db.models.functions import Coalesce, TruncMonth

from clientes.models import Cliente
from habitaciones.models import Habitacion
from reservaciones.models import Reservacion

CERO = Value(Decimal("0.00"), output_field=DecimalField(max_digits=12, decimal_places=2))
NOMBRES_MES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]


def reservaciones_del_periodo(desde, hasta):
    """Reservaciones cuya fecha de entrada cae en el periodo."""
    return Reservacion.objects.filter(fecha_entrada__gte=desde, fecha_entrada__lte=hasta)


def ingresos_totales(qs=None):
    qs = Reservacion.objects.all() if qs is None else qs
    return qs.filter(estado__in=Reservacion.ESTADOS_INGRESO).aggregate(
        total=Coalesce(Sum("total"), CERO)
    )["total"]


def resumen_general(desde, hasta):
    qs = reservaciones_del_periodo(desde, hasta)
    por_estado = {fila["estado"]: fila["n"] for fila in qs.values("estado").annotate(n=Count("id"))}
    cobradas = qs.filter(estado__in=Reservacion.ESTADOS_INGRESO)
    n_cobradas = cobradas.count()
    ingresos = ingresos_totales(qs)
    return {
        "total_reservaciones": qs.count(),
        "ingresos": ingresos,
        "ticket_promedio": (ingresos / n_cobradas) if n_cobradas else Decimal("0"),
        "canceladas": por_estado.get(Reservacion.Estado.CANCELADA, 0),
        "por_estado": [
            {"estado": etiqueta, "clave": clave, "n": por_estado.get(clave, 0)}
            for clave, etiqueta in Reservacion.Estado.choices
        ],
        "clientes_nuevos": Cliente.objects.filter(
            fecha_registro__date__gte=desde, fecha_registro__date__lte=hasta
        ).count(),
    }


def ingresos_por_mes(desde, hasta):
    filas = (
        reservaciones_del_periodo(desde, hasta)
        .filter(estado__in=Reservacion.ESTADOS_INGRESO)
        .annotate(mes=TruncMonth("fecha_entrada"))
        .values("mes")
        .annotate(ingresos=Sum("total"), reservas=Count("id"))
        .order_by("mes")
    )
    return [
        {
            "etiqueta": f"{NOMBRES_MES[f['mes'].month - 1]} {f['mes'].year}",
            "ingresos": f["ingresos"],
            "reservas": f["reservas"],
        }
        for f in filas
    ]


def ingresos_por_tipo(desde, hasta):
    nombres = dict(Habitacion.TIPOS)
    filas = (
        reservaciones_del_periodo(desde, hasta)
        .filter(estado__in=Reservacion.ESTADOS_INGRESO)
        .values("habitacion__tipo")
        .annotate(ingresos=Sum("total"), reservas=Count("id"))
        .order_by("-ingresos")
    )
    return [
        {
            "tipo": nombres.get(f["habitacion__tipo"], f["habitacion__tipo"]),
            "ingresos": f["ingresos"],
            "reservas": f["reservas"],
        }
        for f in filas
    ]


def mejores_clientes(desde, hasta, limite=5):
    return (
        Cliente.objects.filter(
            reservaciones__fecha_entrada__gte=desde,
            reservaciones__fecha_entrada__lte=hasta,
            reservaciones__estado__in=Reservacion.ESTADOS_INGRESO,
        )
        .annotate(reservas=Count("reservaciones"), gastado=Sum("reservaciones__total"))
        .order_by("-gastado")[:limite]
    )


def ocupacion_por_habitacion(desde, hasta):
    """Noches ocupadas de cada habitación dentro del periodo y % de ocupación."""
    dias_periodo = (hasta - desde).days + 1
    fin = hasta + timedelta(days=1)  # el periodo incluye el día "hasta"
    resultado = []
    reservas = Reservacion.objects.filter(
        estado__in=Reservacion.ESTADOS_INGRESO + [Reservacion.Estado.PENDIENTE],
        fecha_entrada__lt=fin,
        fecha_salida__gt=desde,
    )
    noches = {}
    for r in reservas:
        inicio = max(r.fecha_entrada, desde)
        final = min(r.fecha_salida, fin)
        noches[r.habitacion_id] = noches.get(r.habitacion_id, 0) + (final - inicio).days
    for h in Habitacion.objects.order_by("numero"):
        n = noches.get(h.pk, 0)
        resultado.append(
            {
                "habitacion": h,
                "noches": n,
                "porcentaje": round(n * 100 / dias_periodo, 1) if dias_periodo else 0,
            }
        )
    total_noches = sum(f["noches"] for f in resultado)
    capacidad = dias_periodo * len(resultado)
    tasa = round(total_noches * 100 / capacidad, 1) if capacidad else 0
    return resultado, tasa
