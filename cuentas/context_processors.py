"""Variables disponibles en TODOS los templates - Integrante 5."""

from .permisos import es_administrador, nombre_rol


def rol_usuario(request):
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return {"es_admin": False, "rol_usuario": ""}
    return {"es_admin": es_administrador(user), "rol_usuario": nombre_rol(user)}
