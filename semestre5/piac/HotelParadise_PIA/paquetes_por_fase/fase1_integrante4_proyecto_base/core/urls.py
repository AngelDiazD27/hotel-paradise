"""Rutas de core (dashboard) - Integrante 4."""

from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
]
