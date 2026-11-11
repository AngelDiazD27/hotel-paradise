"""Rutas del módulo Habitaciones - Integrante 1."""

from django.urls import path

from . import views

app_name = "habitaciones"  # Permite usar {% url 'habitaciones:lista' %}

urlpatterns = [
    path("", views.HabitacionListView.as_view(), name="lista"),
    path("nueva/", views.HabitacionCreateView.as_view(), name="crear"),
    path("<int:pk>/", views.HabitacionDetailView.as_view(), name="detalle"),
    path("<int:pk>/editar/", views.HabitacionUpdateView.as_view(), name="editar"),
    path("<int:pk>/eliminar/", views.HabitacionDeleteView.as_view(), name="eliminar"),
]
