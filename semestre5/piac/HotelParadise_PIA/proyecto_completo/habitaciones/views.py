"""
Vistas del módulo Habitaciones - Integrante 1.

Se usan vistas basadas en clases (CBV) genéricas de Django:
  ListView   -> Consultar (lista con búsqueda)
  DetailView -> Consultar (detalle)
  CreateView -> Crear
  UpdateView -> Modificar
  DeleteView -> Eliminar (con la Regla 5)

PermisoRequeridoMixin (core/mixins.py) -> obliga a iniciar sesión y revisa
que el rol del usuario tenga el permiso indicado en `permission_required`.
"""

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from core.mixins import PermisoRequeridoMixin

from .forms import BusquedaHabitacionForm, HabitacionForm
from .models import Habitacion


class HabitacionListView(PermisoRequeridoMixin, ListView):
    model = Habitacion
    permission_required = "habitaciones.view_habitacion"
    template_name = "habitaciones/lista.html"
    context_object_name = "habitaciones"
    paginate_by = 9

    def get_queryset(self):
        qs = super().get_queryset()
        self.form = BusquedaHabitacionForm(self.request.GET or None)
        if self.form.is_valid():
            q = self.form.cleaned_data.get("q")
            tipo = self.form.cleaned_data.get("tipo")
            disponible = self.form.cleaned_data.get("disponible")
            if q:
                filtro = Q(descripcion__icontains=q)
                if q.isdigit():
                    filtro |= Q(numero=int(q))
                qs = qs.filter(filtro)
            if tipo:
                qs = qs.filter(tipo=tipo)
            if disponible in ("0", "1"):
                qs = qs.filter(disponible=(disponible == "1"))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = self.form
        # Conserva los filtros al cambiar de página.
        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["querystring"] = params.urlencode()
        return ctx


class HabitacionDetailView(PermisoRequeridoMixin, DetailView):
    model = Habitacion
    permission_required = "habitaciones.view_habitacion"
    template_name = "habitaciones/detalle.html"
    context_object_name = "habitacion"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["reservaciones_activas"] = self.object.reservaciones_activas()
        return ctx


class HabitacionCreateView(PermisoRequeridoMixin, SuccessMessageMixin, CreateView):
    model = Habitacion
    form_class = HabitacionForm
    permission_required = "habitaciones.add_habitacion"
    template_name = "habitaciones/formulario.html"
    success_message = "La habitación %(numero)s se registró correctamente."


class HabitacionUpdateView(PermisoRequeridoMixin, SuccessMessageMixin, UpdateView):
    model = Habitacion
    form_class = HabitacionForm
    permission_required = "habitaciones.change_habitacion"
    template_name = "habitaciones/formulario.html"
    success_message = "La habitación %(numero)s se actualizó correctamente."


class HabitacionDeleteView(PermisoRequeridoMixin, SuccessMessageMixin, DeleteView):
    model = Habitacion
    permission_required = "habitaciones.delete_habitacion"
    template_name = "habitaciones/confirmar_eliminar.html"
    context_object_name = "habitacion"
    success_url = reverse_lazy("habitaciones:lista")
    success_message = "La habitación se eliminó correctamente."

    def form_valid(self, form):
        # Regla 5: no se puede eliminar una habitación con reservaciones activas.
        if self.object.tiene_reservaciones_activas():
            messages.error(
                self.request,
                f"No se puede eliminar la habitación {self.object.numero}: "
                "tiene reservaciones activas. Cancélalas o espera a que terminen.",
            )
            return redirect(self.object.get_absolute_url())
        return super().form_valid(form)
