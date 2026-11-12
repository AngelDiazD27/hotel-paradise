"""Vistas del módulo Clientes (CRUD + búsqueda) - Integrante 2."""

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from core.mixins import PermisoRequeridoMixin

from .forms import BusquedaClienteForm, ClienteForm
from .models import Cliente


class ClienteListView(PermisoRequeridoMixin, ListView):
    model = Cliente
    permission_required = "clientes.view_cliente"
    template_name = "clientes/lista.html"
    context_object_name = "clientes"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        self.form = BusquedaClienteForm(self.request.GET or None)
        if self.form.is_valid() and self.form.cleaned_data.get("q"):
            q = self.form.cleaned_data["q"].strip()
            # Búsqueda en varios campos con Q (OR). Si escriben "Ana López"
            # se busca cada palabra por separado.
            for palabra in q.split():
                qs = qs.filter(
                    Q(nombre__icontains=palabra)
                    | Q(apellidos__icontains=palabra)
                    | Q(correo__icontains=palabra)
                    | Q(telefono__icontains=palabra)
                )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = self.form
        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["querystring"] = params.urlencode()
        return ctx


class ClienteDetailView(PermisoRequeridoMixin, DetailView):
    model = Cliente
    permission_required = "clientes.view_cliente"
    template_name = "clientes/detalle.html"
    context_object_name = "cliente"


class ClienteCreateView(PermisoRequeridoMixin, SuccessMessageMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    permission_required = "clientes.add_cliente"
    template_name = "clientes/formulario.html"
    success_message = "El cliente %(nombre)s %(apellidos)s se registró correctamente."


class ClienteUpdateView(PermisoRequeridoMixin, SuccessMessageMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    permission_required = "clientes.change_cliente"
    template_name = "clientes/formulario.html"
    success_message = "Los datos de %(nombre)s %(apellidos)s se actualizaron."


class ClienteDeleteView(PermisoRequeridoMixin, SuccessMessageMixin, DeleteView):
    model = Cliente
    permission_required = "clientes.delete_cliente"
    template_name = "clientes/confirmar_eliminar.html"
    context_object_name = "cliente"
    success_url = reverse_lazy("clientes:lista")
    success_message = "El cliente se eliminó correctamente."

    def form_valid(self, form):
        if self.object.tiene_reservaciones_activas():
            messages.error(
                self.request,
                f"No se puede eliminar a {self.object}: tiene reservaciones activas.",
            )
            return redirect(self.object.get_absolute_url())
        return super().form_valid(form)
