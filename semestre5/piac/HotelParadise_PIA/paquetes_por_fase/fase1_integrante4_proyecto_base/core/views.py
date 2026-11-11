"""
Página de inicio provisional - Integrante 4 (Fase 1).

En esta fase todavía no existen los demás módulos, así que el "dashboard"
sólo muestra qué módulos ya se instalaron. En la Fase 7 este archivo se
reemplaza por el dashboard final con estadísticas.
"""

from django.views.generic import TemplateView


class DashboardView(TemplateView):
    template_name = "core/dashboard.html"
