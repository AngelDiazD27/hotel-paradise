"""
Comando: python manage.py crear_roles      - Integrante 5

Crea (o actualiza) los grupos Administrador y Recepcionista con sus permisos.
Se puede ejecutar las veces que sea necesario.
"""

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from cuentas.permisos import PERMISOS_POR_ROL


class Command(BaseCommand):
    help = "Crea los roles (grupos) del sistema con sus permisos."

    def handle(self, *args, **options):
        hablar = options["verbosity"] > 0  # --verbosity 0 = modo silencioso
        for rol, reglas in PERMISOS_POR_ROL.items():
            grupo, creado = Group.objects.get_or_create(name=rol)
            permisos = []
            for app, modelo, acciones in reglas:
                for accion in acciones:
                    codename = f"{accion}_{modelo}"
                    try:
                        permisos.append(
                            Permission.objects.get(content_type__app_label=app, codename=codename)
                        )
                    except Permission.DoesNotExist:
                        if hablar:
                            self.stdout.write(
                                self.style.WARNING(f"  Falta el permiso {app}.{codename} (¿ya migraste esa app?)")
                            )
            grupo.permissions.set(permisos)
            estado = "creado" if creado else "actualizado"
            if hablar:
                self.stdout.write(self.style.SUCCESS(f"Rol '{rol}' {estado} con {len(permisos)} permisos."))
