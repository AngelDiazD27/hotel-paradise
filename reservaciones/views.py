"""
Vistas del módulo Reservaciones - Integrante 3.

  * Lista con búsqueda por cliente, habitación, tipo y estado.
  * Registrar, consultar, modificar y CANCELAR (no se borran, se cancelan).
  * Consulta de disponibilidad por fechas.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.mixins import PermisoRequeridoMixin
from habitaciones.models import Habitacion

from .forms import BusquedaReservacionForm, DisponibilidadForm, ReservacionForm
from .models import Reservacion


class ReservacionListView(PermisoRequeridoMixin, ListView):
    model = Reservacion
    permission_required = "reservaciones.view_reservacion"
    template_name = "reservaciones/lista.html"
    context_object_name = "reservaciones"
    paginate_by = 12

    def get_queryset(self):
        # select_related evita una consulta extra por cada fila (JOIN).
        qs = Reservacion.objects.select_related("cliente", "habitacion")
        self.form = BusquedaReservacionForm(self.request.GET or None)
        if self.form.is_valid():
            d = self.form.cleaned_data
            if d.get("cliente"):
                for palabra in d["cliente"].split():
                    qs = qs.filter(
                        Q(cliente__nombre__icontains=palabra)
                        | Q(cliente__apellidos__icontains=palabra)
                        | Q(cliente__correo__icontains=palabra)
                    )
            if d.get("habitacion"):
                qs = qs.filter(habitacion__numero=d["habitacion"])
            if d.get("tipo"):
                qs = qs.filter(habitacion__tipo=d["tipo"])
            if d.get("estado"):
                qs = qs.filter(estado=d["estado"])
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = self.form
        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["querystring"] = params.urlencode()
        return ctx


class ReservacionDetailView(PermisoRequeridoMixin, DetailView):
    model = Reservacion
    permission_required = "reservaciones.view_reservacion"
    template_name = "reservaciones/detalle.html"
    context_object_name = "reservacion"

    def get_queryset(self):
        return Reservacion.objects.select_related("cliente", "habitacion")


class ReservacionCreateView(PermisoRequeridoMixin, SuccessMessageMixin, CreateView):
    model = Reservacion
    form_class = ReservacionForm
    permission_required = "reservaciones.add_reservacion"
    template_name = "reservaciones/formulario.html"

    def get_initial(self):
        """Permite llegar desde "Disponibilidad" o desde un cliente con datos ya llenos."""
        inicial = super().get_initial()
        for campo in ("cliente", "habitacion", "fecha_entrada", "fecha_salida", "num_huespedes"):
            valor = self.request.GET.get(campo)
            if valor:
                inicial[campo] = valor
        return inicial

    def get_success_message(self, cleaned_data):
        r = self.object
        return (
            f"Reservación #{r.pk} registrada: habitación {r.habitacion.numero}, "
            f"{r.noches} noche(s), total ${r.total:,.2f}."
        )


class ReservacionUpdateView(PermisoRequeridoMixin, SuccessMessageMixin, UpdateView):
    model = Reservacion
    form_class = ReservacionForm
    permission_required = "reservaciones.change_reservacion"
    template_name = "reservaciones/formulario.html"

    def get_success_message(self, cleaned_data):
        return f"Reservación #{self.object.pk} actualizada. Nuevo total: ${self.object.total:,.2f}."


@login_required
@permission_required("reservaciones.change_reservacion", raise_exception=True)
@require_http_methods(["GET", "POST"])
def cancelar_reservacion(request, pk):
    """Cancelar = cambiar el estado a CANCELADA. El registro se conserva como historial."""
    reservacion = get_object_or_404(Reservacion, pk=pk)
    if not reservacion.puede_cancelarse:
        messages.warning(request, "Esta reservación ya no se puede cancelar.")
        return redirect(reservacion)
    if request.method == "POST":
        reservacion.estado = Reservacion.Estado.CANCELADA
        reservacion.save(update_fields=["estado", "total", "actualizada"])
        messages.success(
            request,
            f"La reservación #{reservacion.pk} fue cancelada. "
            f"La habitación {reservacion.habitacion.numero} queda libre en esas fechas.",
        )
        return redirect(reservacion)
    return render(request, "reservaciones/confirmar_cancelar.html", {"reservacion": reservacion})


@login_required
@permission_required("reservaciones.view_reservacion", raise_exception=True)
def disponibilidad(request):
    """Muestra las habitaciones libres para un rango de fechas."""
    form = DisponibilidadForm(request.GET or None)
    libres = None
    if form.is_valid():
        d = form.cleaned_data
        entrada, salida = d["fecha_entrada"], d["fecha_salida"]
        # Habitaciones ocupadas en ese rango (subconsulta)
        ocupadas = Reservacion.objects.filter(
            estado__in=Reservacion.ESTADOS_ACTIVOS,
            fecha_entrada__lt=salida,
            fecha_salida__gt=entrada,
        ).values("habitacion_id")
        libres = Habitacion.objects.filter(
            disponible=True, capacidad__gte=d["huespedes"]
        ).exclude(pk__in=ocupadas)
        if d.get("tipo"):
            libres = libres.filter(tipo=d["tipo"])
        libres = libres.order_by("precio_noche", "numero")
        noches = (salida - entrada).days
        for h in libres:
            h.total_estimado = h.precio_noche * noches
        return render(
            request,
            "reservaciones/disponibilidad.html",
            {"form": form, "libres": libres, "noches": noches, "datos": d},
        )
    return render(request, "reservaciones/disponibilidad.html", {"form": form, "libres": libres})
