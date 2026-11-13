# Hotel Paradise · Sistema de Reservación de Hotel

Aplicación web en **Django 5.2** para administrar habitaciones, clientes y reservaciones de la cadena Hotel Paradise.
PIA de *Fundamentos del Desarrollo Web* (UANL · FACPYA).

## Qué hace

- **Habitaciones**: CRUD con fotografía, tipos (Individual, Doble, Suite, Presidencial), búsqueda por número y tipo.
- **Clientes**: CRUD con correo único, validación de teléfono y búsqueda por nombre, correo o teléfono.
- **Reservaciones**: registrar, consultar, modificar y cancelar; total calculado automáticamente; consulta de disponibilidad por fechas.
- **Dashboard**: total de clientes, habitaciones, reservaciones, habitaciones disponibles e ingresos generados, más un tablero con el estado de cada habitación.
- **Seguridad y reportes**: login/logout, roles *Administrador* y *Recepcionista*, gestión de usuarios, reportes con gráficas y exportación a CSV.

## Reglas de negocio

| # | Regla | Dónde se valida |
|---|-------|-----------------|
| 1 | Una habitación no se reserva dos veces en las mismas fechas | `Reservacion.clean()` |
| 2 | La fecha de salida debe ser mayor que la de entrada | `Reservacion.clean()` + `CheckConstraint` en la BD |
| 3 | No se repiten números de habitación | `Habitacion.numero` (`unique=True`) |
| 4 | El correo del cliente es único | `Cliente.correo` (`unique=True`) + `ClienteForm.clean_correo()` |
| 5 | No se elimina una habitación con reservaciones activas | `HabitacionDeleteView.form_valid()` y el Django Admin |

## Cómo ejecutarlo

Requisitos: Python 3.10 o superior y Git.

```bash
git clone https://github.com/USUARIO/hotel-paradise.git
cd hotel-paradise

python -m venv venv
# Windows:  venv\Scripts\activate
# macOS / Linux:  source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py cargar_demo        # datos de ejemplo + usuarios + roles
python manage.py runserver
```

Abre <http://127.0.0.1:8000> e inicia sesión:

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| `admin` | `Paradise2026!` | Administrador (acceso total y Django Admin) |
| `recepcion` | `Recepcion2026!` | Recepcionista (clientes y reservaciones) |

Para empezar sin datos de ejemplo: `python manage.py crear_roles` y `python manage.py createsuperuser`.

Pruebas automáticas: `python manage.py test` (36 pruebas).

## Estructura

```
hotel_paradise/   configuración (settings.py, urls.py)
core/             dashboard, plantilla base, mixins       · Integrante 4
cuentas/          login, logout, roles y usuarios         · Integrante 5
habitaciones/     modelo y CRUD de habitaciones           · Integrante 1
clientes/         modelo y CRUD de clientes               · Integrante 2
reservaciones/    modelo, CRUD y disponibilidad           · Integrante 3
reportes/         estadísticas y exportación CSV          · Integrante 5
templates/        base.html, parciales, páginas 403/404
static/           Bootstrap 5, íconos, Chart.js y estilos propios (sin depender de internet)
docs/             documento técnico, manual de usuario y guía del equipo
```

## Equipo

| Integrante | Módulo |
|------------|--------|
| Integrante 1 · *[Nombre]* | Habitaciones |
| Integrante 2 · *[Nombre]* | Clientes |
| Integrante 3 · *[Nombre]* | Reservaciones |
| Integrante 4 · *[Nombre]* | Interfaz web y dashboard |
| Integrante 5 · *[Nombre]* | Seguridad y reportes |
