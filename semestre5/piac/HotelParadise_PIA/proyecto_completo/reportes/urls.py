"""Rutas de reportes - Integrante 5."""

from django.urls import path

from . import views

app_name = "reportes"

urlpatterns = [
    path("", views.ReporteView.as_view(), name="general"),
    path("exportar/", views.ExportarCSVView.as_view(), name="exportar_csv"),
]
