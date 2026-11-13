"""Rutas del módulo Reservaciones - Integrante 3."""

from django.urls import path

from . import views

app_name = "reservaciones"

urlpatterns = [
    path("", views.ReservacionListView.as_view(), name="lista"),
    path("nueva/", views.ReservacionCreateView.as_view(), name="crear"),
    path("disponibilidad/", views.disponibilidad, name="disponibilidad"),
    path("<int:pk>/", views.ReservacionDetailView.as_view(), name="detalle"),
    path("<int:pk>/editar/", views.ReservacionUpdateView.as_view(), name="editar"),
    path("<int:pk>/cancelar/", views.cancelar_reservacion, name="cancelar"),
]
