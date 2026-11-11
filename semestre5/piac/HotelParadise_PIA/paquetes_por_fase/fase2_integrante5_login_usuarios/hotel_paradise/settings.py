"""
Configuración del proyecto Hotel Paradise.

Cada bloque está marcado con el integrante responsable, para que el equipo
sepa quién agregó cada parte y por qué.

Documentación oficial: https://docs.djangoproject.com/es/5.2/ref/settings/
"""

from pathlib import Path

# BASE_DIR apunta a la carpeta raíz del proyecto (donde está manage.py).
BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Seguridad básica (Integrante 4 - proyecto base)
# ---------------------------------------------------------------------------
# ADVERTENCIA: esta clave sólo sirve para desarrollo. En producción se lee de
# una variable de entorno y nunca se sube a GitHub.
SECRET_KEY = "django-insecure-hotel-paradise-pia-cambiar-en-produccion"

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


# ---------------------------------------------------------------------------
# Aplicaciones instaladas
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    # Apps que trae Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Apps del proyecto (una por integrante)
    "core",            # Integrante 4 - Interfaz web y dashboard
    "cuentas",         # Integrante 5 - Login, logout y usuarios
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hotel_paradise.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Carpeta global de templates (base.html, login, errores).
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                # Qué módulos están instalados, para armar el menú (Integrante 4).
                "core.context_processors.modulos_instalados",
                # Agrega `es_admin` y `rol_usuario` a todos los templates (Integrante 5).
                "cuentas.context_processors.rol_usuario",
            ],
        },
    },
]

WSGI_APPLICATION = "hotel_paradise.wsgi.application"


# ---------------------------------------------------------------------------
# Base de datos: SQLite (requerimiento técnico del PIA)
# ---------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ---------------------------------------------------------------------------
# Contraseñas
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ---------------------------------------------------------------------------
# Idioma y zona horaria: español de México
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "es-mx"
TIME_ZONE = "America/Monterrey"
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------------------------------
# Archivos estáticos (CSS, JS, Bootstrap local) - Integrante 4
# ---------------------------------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]




# ---------------------------------------------------------------------------
# Autenticación - Integrante 5
# ---------------------------------------------------------------------------
LOGIN_URL = "cuentas:login"            # A dónde se manda a quien no ha iniciado sesión
LOGIN_REDIRECT_URL = "core:dashboard"  # A dónde va después de iniciar sesión
LOGOUT_REDIRECT_URL = "cuentas:login"  # A dónde va después de cerrar sesión


# ---------------------------------------------------------------------------
# Mensajes con clases de Bootstrap (alert-danger en lugar de alert-error)
# ---------------------------------------------------------------------------
from django.contrib.messages import constants as message_constants  # noqa: E402

MESSAGE_TAGS = {message_constants.ERROR: "danger"}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
