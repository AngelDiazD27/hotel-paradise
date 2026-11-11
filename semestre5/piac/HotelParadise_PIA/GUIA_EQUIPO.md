---
title: "Guía del equipo — PIA Hotel Paradise (Django)"
subtitle: "Cómo construir, subir a GitHub y presentar el proyecto paso a paso, entre 5 integrantes"
---

# 1. Lo que van a construir

Una aplicación web en **Django 5.2** para la cadena **Hotel Paradise**. El personal del hotel inicia sesión, consulta qué habitaciones están libres, registra clientes y hace reservaciones sin que una habitación se reserve dos veces en las mismas fechas. Un administrador además ve reportes de ingresos y da de alta a otros usuarios.

El sistema ya está terminado y probado (35 pruebas automáticas). Lo que sigue en esta guía es **cómo lo arma el equipo en GitHub**, cada quien su parte, de forma que:

- cada integrante tenga **sus propios commits** (la rúbrica lo revisa),
- el proyecto **funcione al final de cada fase**, no sólo al final,
- todos **entiendan** lo que subieron y lo puedan explicar en el video.

## 1.1 El flujo de Django que van a dominar

Cada pantalla del sistema sigue este camino. Es la "Meta final" del PIA y conviene que todos lo sepan explicar con un ejemplo:

```
Usuario  →  URL  →  Vista  →  Formulario  →  Modelo  →  Base de datos  →  Template  →  Navegador
```

**Ejemplo: registrar una reservación**

| Paso | Archivo | Qué pasa |
|------|---------|----------|
| URL | `reservaciones/urls.py` | `/reservaciones/nueva/` se conecta con `ReservacionCreateView` |
| Vista | `reservaciones/views.py` | Revisa que el usuario tenga sesión y permiso; muestra o procesa el formulario |
| Formulario | `reservaciones/forms.py` | `ReservacionForm` valida los datos que escribió el usuario |
| Modelo | `reservaciones/models.py` | `Reservacion.clean()` aplica las Reglas 1 y 2; `save()` calcula el total |
| Base de datos | `db.sqlite3` | Django ejecuta el `INSERT` por nosotros (ORM) |
| Template | `reservaciones/templates/reservaciones/formulario.html` | Dibuja el formulario con Bootstrap y muestra los errores |

## 1.2 Reparto de roles

| Integrante | Módulo | Apps / carpetas que le pertenecen | Fases |
|---|---|---|---|
| **Integrante 1** | Habitaciones | `habitaciones/` (modelo, CRUD, fotos, admin) | Fase 3 |
| **Integrante 2** | Clientes | `clientes/` (modelo, CRUD, validación de correo, búsqueda) | Fase 4 |
| **Integrante 3** | Reservaciones | `reservaciones/` (modelo, registro, fechas, disponibilidad) | Fase 5 |
| **Integrante 4** | Interfaz web | Proyecto base, `core/`, `templates/`, `static/`, dashboard | Fases 1 y 7 |
| **Integrante 5** | Seguridad y reportes | `cuentas/` (login, logout, roles, usuarios) y `reportes/` | Fases 2 y 6 |
| **Todos** | Documentación y video | `docs/` y conclusión individual | Fase 8 |

> **Integrante 4 es el "dueño" del repositorio**: lo crea en GitHub e invita a los demás. Cualquiera puede serlo, pero conviene que sea quien hace la Fase 1.

## 1.3 Las fases y por qué van en este orden

Cada módulo depende de los anteriores (una reservación necesita un cliente y una habitación; el dashboard necesita todo). Por eso se sube **una fase a la vez**, en este orden:

| Fase | Quién | Qué sube | Depende de |
|---|---|---|---|
| 1 | Integrante 4 | Proyecto base, plantilla, Bootstrap, estilos | — |
| 2 | Integrante 5 | Login, logout, roles, usuarios | Fase 1 |
| 3 | Integrante 1 | Módulo Habitaciones | Fase 2 |
| 4 | Integrante 2 | Módulo Clientes | Fase 3 |
| 5 | Integrante 3 | Módulo Reservaciones | Fases 3 y 4 |
| 6 | Integrante 5 | Reportes, estadísticas, comando de roles | Fase 5 |
| 7 | Integrante 4 | Dashboard final, datos de demostración, README | Fase 6 |
| 8 | Todos | Documento técnico, manual, capturas, conclusiones | Fase 7 |

**Mientras esperan su turno no están parados:** cada quien abre su paquete (carpeta `paquetes_por_fase/`), lee el código con calma, lo corre en una copia aparte si quiere, y prepara lo que va a explicar en el video. Cuando le toca, sube su fase en 20–30 minutos.

Un calendario realista:

| Día | Qué se hace |
|---|---|
| Día 1 | Todos instalan herramientas (sección 2). Integrante 4 crea el repo y sube la Fase 1. Integrante 5 sube la Fase 2. |
| Día 2 | Integrante 1 sube la Fase 3. Integrante 2 sube la Fase 4. |
| Día 3 | Integrante 3 sube la Fase 5. Integrante 5 sube la Fase 6. |
| Día 4 | Integrante 4 sube la Fase 7. Todos hacen la Fase 8 (documentos y capturas). |
| Día 5 | Grabación del video y revisión final. |

## 1.4 Qué hay en la carpeta que reciben

```
HotelParadise_PIA/
├── GUIA_EQUIPO.docx / .md        ← esta guía
├── paquetes_por_fase/            ← lo que cada integrante copia a su repo en su turno
│   ├── fase1_integrante4_proyecto_base/
│   ├── fase2_integrante5_login_usuarios/
│   ├── fase3_integrante1_habitaciones/
│   ├── fase4_integrante2_clientes/
│   ├── fase5_integrante3_reservaciones/
│   ├── fase6_integrante5_reportes/
│   ├── fase7_integrante4_dashboard/
│   └── fase8_todos_documentacion/
├── proyecto_completo/            ← el sistema terminado, para correrlo y compararlo
└── entregables/                  ← documento técnico, manual de usuario y diagramas
```

Cada paquete contiene **sólo los archivos de esa fase**, con las mismas rutas que tendrán en el repositorio. Los archivos compartidos (`settings.py`, `urls.py`, `requirements.txt`) vienen en la versión exacta que corresponde a esa fase: ya traen las líneas de los integrantes anteriores más las tuyas.

# 2. Preparación (todos, una sola vez)

## 2.1 Instalar las herramientas

1. **Python 3.12 o 3.13** desde <https://www.python.org/downloads/>. En Windows marca la casilla **"Add python.exe to PATH"** en la primera pantalla del instalador.
2. **Git** desde <https://git-scm.com/downloads> (en Windows deja todas las opciones por defecto).
3. **Visual Studio Code** desde <https://code.visualstudio.com/> con la extensión *Python* de Microsoft.
4. Una **cuenta de GitHub** en <https://github.com/>. Usen de preferencia su correo de la UANL.

Comprueba en una terminal (en Windows: *PowerShell* o la terminal de VS Code):

```bash
python --version      # Python 3.12.x o 3.13.x
git --version         # git version 2.x
```

> En macOS / Linux el comando puede ser `python3` en lugar de `python`.

## 2.2 Configurar Git con TU nombre y TU correo

Esto es lo que hace que los commits aparezcan a tu nombre en GitHub. **El correo debe ser el mismo de tu cuenta de GitHub**; si no, tus commits no se cuentan como tuyos en *Insights → Contributors*.

```bash
git config --global user.name "Tu Nombre Apellido"
git config --global user.email "tu_correo_de_github@uanl.edu.mx"
git config --global init.defaultBranch main
```

## 2.3 Cómo sube Git los cambios (lo mínimo que hay que entender)

| Concepto | Qué es |
|---|---|
| **Repositorio** | La carpeta del proyecto con todo su historial. Hay una copia en GitHub (`origin`) y una en tu computadora. |
| **Commit** | Una "foto" de los cambios con un mensaje que dice qué hiciste. |
| **Rama (branch)** | Una línea de trabajo aparte. `main` es la versión oficial; cada quien trabaja en su rama `feature/...`. |
| **Push** | Subir tus commits a GitHub. |
| **Pull** | Bajar a tu computadora lo que otros subieron. |
| **Pull Request (PR)** | Pedirle al equipo que revise tu rama y la una a `main`. Es la evidencia de trabajo en equipo. |

El ciclo que cada integrante repite en su turno:

```
git pull  →  git checkout -b feature/mi-modulo  →  copiar archivos  →  probar
        →  git add + git commit (varias veces)  →  git push  →  Pull Request  →  Merge
```

# 3. Crear el repositorio en GitHub (Integrante 4)

1. Entra a GitHub → botón **New** (o <https://github.com/new>).
2. **Repository name:** `hotel-paradise`
3. **Description:** `PIA Django - Sistema de reservación de hotel`
4. Visibilidad: **Public** (o Private si el profesor lo pide; entonces agrégalo como colaborador).
5. **NO** marques "Add a README", ni ".gitignore", ni licencia. El repo debe nacer vacío; el `.gitignore` viene en la Fase 1 y el README en la Fase 7.
6. Clic en **Create repository**.

Invita al equipo: **Settings → Collaborators → Add people**, escribe el usuario de GitHub de cada integrante. Cada uno debe **aceptar la invitación** desde su correo o desde <https://github.com/notifications>.

Opcional pero recomendado (da puntos en "uso adecuado de Git"), **después de subir la Fase 1**: **Settings → Rules → Rulesets → New branch ruleset**, objetivo `main` (*Include default branch*), activando *Require a pull request before merging*. Así nadie sube directo a `main` sin revisión.

# 4. Fase por fase

Cada fase tiene la misma estructura: **qué aprendes**, **pasos**, **cómo verificar** y **commits**. Los comandos están para Windows (PowerShell); en macOS / Linux cambia `venv\Scripts\activate` por `source venv/bin/activate` y `python` por `python3`.

> **Regla de oro:** antes de hacer commit, abre cada archivo que copiaste y lee los comentarios. Todo el código está comentado en español explicando qué hace cada parte. En el video te van a preguntar por *tu* código.

## Fase 1 — Integrante 4: proyecto base

**Qué aprendes:** estructura de un proyecto Django (`manage.py`, `settings.py`, `urls.py`), apps, plantillas con herencia (`{% extends %}` y `{% block %}`), archivos estáticos, Bootstrap 5 y diseño responsivo.

**Pasos**

```powershell
# 1. Crea una carpeta de trabajo y clona el repo vacío
cd $HOME\Documents
git clone https://github.com/USUARIO/hotel-paradise.git
cd hotel-paradise

# 2. La Fase 1 se sube directo a main: el repo está vacío y todavía no hay
#    nada contra qué comparar en un Pull Request. Desde la Fase 2 se usan ramas.
git checkout -b main      # si dice que main ya existe, ignóralo

# 3. Entorno virtual (una "caja" con las librerías de este proyecto)
python -m venv venv
venv\Scripts\activate
#   Si PowerShell dice que no puede ejecutar scripts:
#   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned   (y vuelve a activar)

# 4. Copia TODO el contenido de paquetes_por_fase\fase1_integrante4_proyecto_base\
#    dentro de la carpeta hotel-paradise (puedes arrastrarlo con el Explorador)
Copy-Item -Recurse -Force "RUTA\paquetes_por_fase\fase1_integrante4_proyecto_base\*" .

# 5. Instala Django y crea la base de datos
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

> Si quieres hacerlo "desde cero" para aprender: `pip install django`, `django-admin startproject hotel_paradise .` y `python manage.py startapp core`, y luego reemplaza los archivos generados con los del paquete. El resultado es el mismo.

**Cómo verificar:** abre <http://127.0.0.1:8000>. Debe aparecer la página "Hotel Paradise" con el menú lateral índigo y la lista "Avance del equipo" con todo en *Pendiente* menos tu parte. Detén el servidor con `Ctrl + C`.

**Archivos clave que debes saber explicar**

| Archivo | Para qué sirve |
|---|---|
| `hotel_paradise/settings.py` | Configuración: apps instaladas, base de datos SQLite, idioma `es-mx`, zona horaria, carpetas de templates y estáticos |
| `templates/base.html` | Plantilla padre: menú lateral, barra superior, mensajes y el `{% block contenido %}` que llenan las demás páginas |
| `static/css/hotel.css` | Colores, tipografías y componentes propios encima de Bootstrap |
| `static/vendor/` | Bootstrap 5, Bootstrap Icons, Chart.js y fuentes guardados localmente: el sistema funciona sin internet |
| `core/context_processors.py` | Le dice al menú qué módulos ya están instalados, para que cada sección aparezca cuando su integrante la suba |
| `core/forms.py` | `BootstrapFormMixin`: pone las clases de Bootstrap a todos los formularios automáticamente |
| `core/mixins.py` | `PermisoRequeridoMixin`: manda al login a quien no ha iniciado sesión y muestra 403 a quien no tiene permiso |
| `.gitignore` | Evita subir `venv/`, `db.sqlite3`, `media/` y `__pycache__/` |

**Commits** (copia y pega uno por uno):

```powershell
git add manage.py .gitignore requirements.txt hotel_paradise/
git commit -m "chore: proyecto Django base con SQLite, idioma es-mx y .gitignore"

git add core/
git commit -m "feat(core): app core con mixins, formularios base y página de inicio"

git add templates/ static/
git commit -m "feat(ui): plantilla base con menú lateral, Bootstrap 5 local y estilos del hotel"

git status          # no debe aparecer venv/ ni db.sqlite3
git push -u origin main
```

Recarga la página del repo en GitHub: deben verse las carpetas y tus 3 commits. Desde aquí, todas las demás fases usan rama propia y Pull Request.

## Cómo es el turno de los demás (Fases 2 a 7)

Todas las fases siguientes usan exactamente esta receta. Sólo cambian el nombre de la rama, el paquete y los commits.

```powershell
# 0. La primera vez: clona el repo y crea tu entorno virtual
git clone https://github.com/USUARIO/hotel-paradise.git
cd hotel-paradise
python -m venv venv

# 1. Cada vez que empiezas: activa el entorno y baja lo último de main
venv\Scripts\activate
git checkout main
git pull
pip install -r requirements.txt
python manage.py migrate

# 2. Tu rama
git checkout -b feature/NOMBRE

# 3. Copia el contenido de tu paquete encima de la carpeta del repo
Copy-Item -Recurse -Force "RUTA\paquetes_por_fase\faseN_...\*" .

# 4. Si tu fase crea un modelo, genera su migración y aplícala
python manage.py makemigrations NOMBRE_APP
python manage.py migrate

# 5. Prueba: corre las pruebas y abre el sistema en el navegador
python manage.py test
python manage.py runserver

# 6. Commits (los de tu fase, abajo) y push
git push -u origin feature/NOMBRE
```

**Pull Request:** en GitHub aparece el aviso amarillo *"feature/NOMBRE had recent pushes"* → **Compare & pull request** → escribe qué hiciste → en **Reviewers** elige a un compañero → **Create pull request**. El compañero revisa (pestaña *Files changed*), aprueba (**Review changes → Approve**) y da **Merge pull request**. Después, todos hacen `git checkout main` y `git pull`.

> Revisar el PR de otro cuenta como "apoyo al equipo" en la rúbrica individual. Repártanse las revisiones: que cada quien revise al menos un PR.

## Fase 2 — Integrante 5: login, logout y usuarios

**Rama:** `feature/cuentas` · **Paquete:** `fase2_integrante5_login_usuarios`

**Qué aprendes:** autenticación de Django (`django.contrib.auth`), vistas `LoginView` / `LogoutView`, por qué el logout se hace con POST y token CSRF, usuarios y grupos como roles, `context_processors`.

**Qué cambia en archivos compartidos** (el paquete ya los trae así):

- `settings.py`: se agrega `"cuentas"` a `INSTALLED_APPS`, el context processor `cuentas.context_processors.rol_usuario` y el bloque `LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL`.
- `urls.py`: se agrega `path("cuentas/", include("cuentas.urls"))`.

Esta app no tiene modelos propios (usa `User` y `Group` de Django), así que **no** lleva `makemigrations`. Sí crea tu usuario administrador local:

```powershell
python manage.py migrate
python manage.py createsuperuser      # usuario y contraseña que tú quieras
python manage.py runserver
```

**Cómo verificar:** entra a <http://127.0.0.1:8000/cuentas/login/>. Con una contraseña equivocada debe decir "Usuario o contraseña incorrectos". Con la correcta te lleva al inicio, arriba a la derecha aparece tu nombre y el botón **Cerrar sesión**, y en el menú aparece **Usuarios**. Crea un usuario con rol *Recepcionista* desde esa pantalla.

**Archivos clave**

| Archivo | Para qué sirve |
|---|---|
| `cuentas/views.py` | Login y logout heredando de las vistas de Django; lista, alta y edición de usuarios |
| `cuentas/forms.py` | Formulario de login con mensajes en español; alta de usuario con rol |
| `cuentas/permisos.py` | Define los roles y qué puede hacer cada uno; `SoloAdministradorMixin` |
| `cuentas/context_processors.py` | Pone `es_admin` y `rol_usuario` en todas las plantillas |

**Commits**

```powershell
git add cuentas/__init__.py cuentas/apps.py cuentas/models.py cuentas/migrations/ cuentas/forms.py cuentas/urls.py cuentas/views.py cuentas/permisos.py cuentas/context_processors.py cuentas/templates/cuentas/login.html hotel_paradise/
git commit -m "feat(cuentas): login y logout con plantillas propias"

git add cuentas/
git commit -m "feat(cuentas): pantallas de control de usuarios por rol"
```

## Fase 3 — Integrante 1: módulo Habitaciones

**Rama:** `feature/habitaciones` · **Paquete:** `fase3_integrante1_habitaciones`

**Qué aprendes:** modelos y tipos de campo (`PositiveIntegerField`, `DecimalField`, `BooleanField`, `ImageField`), `choices`, `unique=True`, migraciones, `ModelForm` con validaciones `clean_<campo>()`, vistas genéricas (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`), subir imágenes (`enctype="multipart/form-data"`, `MEDIA_ROOT`), Django Admin personalizado.

**Qué cambia en archivos compartidos:** `settings.py` agrega `"habitaciones"` y el bloque `MEDIA_URL` / `MEDIA_ROOT`; `urls.py` agrega la ruta del módulo, el encabezado del admin y el servicio de fotos en desarrollo; `requirements.txt` agrega **Pillow** (la librería para manejar imágenes).

```powershell
pip install -r requirements.txt               # instala Pillow
python manage.py makemigrations habitaciones  # crea habitaciones/migrations/0001_initial.py
python manage.py migrate
python manage.py test habitaciones            # 6 pruebas OK
python manage.py runserver
```

`makemigrations` lee `models.py` y escribe un archivo con las instrucciones para crear la tabla; `migrate` ejecuta esas instrucciones en `db.sqlite3`. Abre el `0001_initial.py` que se generó y fíjate cómo cada campo del modelo se convirtió en una columna.

**Cómo verificar:** en el menú aparece **Habitaciones**. Registra 3 habitaciones con foto (cualquier imagen JPG/PNG menor a 2 MB). Intenta registrar otra con un número repetido: debe salir "Ya existe una habitación con este número" (**Regla 3**). Filtra por tipo. Entra a <http://127.0.0.1:8000/admin/> y revisa el panel de habitaciones con miniaturas.

**Regla 5** (no eliminar habitaciones con reservaciones activas): el código ya está en `HabitacionDeleteView.form_valid()` y en `HabitacionAdmin.has_delete_permission()`, pero sólo se podrá ver funcionando cuando exista el módulo de Reservaciones (Fase 5). Mientras tanto, `Habitacion.tiene_reservaciones_activas()` responde "no" gracias a `apps.is_installed("reservaciones")`.

**Commits**

```powershell
git add habitaciones/__init__.py habitaciones/apps.py habitaciones/models.py habitaciones/migrations/ hotel_paradise/settings.py requirements.txt
git commit -m "feat(habitaciones): modelo Habitacion con número único (Regla 3) y migración"

git add habitaciones/admin.py
git commit -m "feat(habitaciones): panel administrativo con fotos y acciones"

git add habitaciones/forms.py habitaciones/views.py habitaciones/urls.py habitaciones/templates/ hotel_paradise/urls.py
git commit -m "feat(habitaciones): CRUD con búsqueda por tipo y Regla 5 al eliminar"

git add habitaciones/tests.py
git commit -m "test(habitaciones): pruebas del CRUD y validaciones"
```

## Fase 4 — Integrante 2: módulo Clientes

**Rama:** `feature/clientes` · **Paquete:** `fase4_integrante2_clientes`

**Qué aprendes:** `EmailField`, `unique=True` con mensaje propio, `RegexValidator`, `auto_now_add`, sobrescribir `save()` para normalizar datos, validación `clean_correo()` que ignora mayúsculas, búsquedas con `Q` (condiciones OR) e `icontains`, paginación.

```powershell
python manage.py makemigrations clientes
python manage.py migrate
python manage.py test habitaciones clientes   # 13 pruebas OK
python manage.py runserver
```

**Cómo verificar:** en el menú aparece **Clientes**. Registra 3 clientes. Intenta registrar otro con el mismo correo pero en mayúsculas (`ANA@correo.com`): debe rechazarlo (**Regla 4**). Prueba un teléfono de 5 dígitos: debe pedir 10. Busca por apellido, por parte del correo y por teléfono.

**Archivos clave:** `clientes/models.py` (el modelo y `save()` que pasa el correo a minúsculas), `clientes/forms.py` (`clean_correo`, `clean_nombre`), `clientes/views.py` (`get_queryset` con la búsqueda por palabras).

**Commits**

```powershell
git add clientes/__init__.py clientes/apps.py clientes/models.py clientes/migrations/ clientes/admin.py hotel_paradise/settings.py
git commit -m "feat(clientes): modelo Cliente con correo único (Regla 4) y migración"

git add clientes/forms.py clientes/views.py clientes/urls.py clientes/templates/ hotel_paradise/urls.py
git commit -m "feat(clientes): CRUD, validación de correo/teléfono y búsqueda"

git add clientes/tests.py
git commit -m "test(clientes): pruebas de registro, correo único y búsqueda"
```

## Fase 5 — Integrante 3: módulo Reservaciones

**Rama:** `feature/reservaciones` · **Paquete:** `fase5_integrante3_reservaciones`

**Qué aprendes:** relaciones **One-to-Many** con `ForeignKey` y `related_name`, `TextChoices` para el estado, validación de modelo con `clean()` (se ejecuta sola en `form.is_valid()`), `CheckConstraint` a nivel base de datos, consultas con rangos de fechas (`__lt`, `__gt`) y subconsultas (`exclude(pk__in=...)`), `select_related` para evitar consultas repetidas, vistas de función con decoradores, `json_script` para pasar datos a JavaScript.

```powershell
python manage.py makemigrations reservaciones
python manage.py migrate
python manage.py test habitaciones clientes reservaciones   # 24 pruebas OK
python manage.py runserver
```

**La lógica que debes poder explicar en el video** (está en `Reservacion.reservaciones_que_chocan`):

Dos estancias `[entrada, salida)` chocan si `entrada_existente < salida_nueva` **y** `salida_existente > entrada_nueva`. Por eso un huésped que sale el día 10 no choca con otro que entra el día 10. Sólo cuentan las reservaciones *Pendientes* o *Confirmadas*: al cancelar, la habitación queda libre.

**Cómo verificar:**

1. **Disponibilidad** → elige fechas → aparecen sólo las habitaciones libres con el total estimado → **Reservar esta habitación**.
2. Al guardar, el total se calcula solo (noches × precio).
3. Intenta reservar la misma habitación en fechas que se traslapen: "La habitación X ya está reservada del ... al ..." (**Regla 1**).
4. Pon la salida antes que la entrada: "La fecha de salida debe ser mayor que la fecha de entrada" (**Regla 2**).
5. Intenta eliminar la habitación reservada: el sistema lo impide (**Regla 5**, ahora sí visible).
6. Cancela la reservación: queda en el historial como *Cancelada* y la habitación se libera.

**Commits**

```powershell
git add reservaciones/__init__.py reservaciones/apps.py reservaciones/models.py reservaciones/migrations/ reservaciones/admin.py hotel_paradise/settings.py
git commit -m "feat(reservaciones): modelo con relaciones 1:N y Reglas 1 y 2"

git add reservaciones/forms.py reservaciones/views.py reservaciones/urls.py reservaciones/templates/ hotel_paradise/urls.py
git commit -m "feat(reservaciones): registrar, modificar y cancelar reservaciones"

git add reservaciones/tests.py
git commit -m "test(reservaciones): pruebas de traslape, fechas y disponibilidad"
```

## Fase 6 — Integrante 5: reportes, estadísticas y roles

**Rama:** `feature/reportes` · **Paquete:** `fase6_integrante5_reportes`

**Qué aprendes:** consultas avanzadas con el ORM: `aggregate(Sum)`, `annotate(Count)`, `values()` para agrupar (equivale a `GROUP BY`), `TruncMonth`, `Coalesce`; comandos propios de `manage.py`; permisos de Django; descargar archivos CSV; gráficas con Chart.js.

```powershell
python manage.py migrate
python manage.py crear_roles     # crea los grupos Administrador y Recepcionista con sus permisos
python manage.py test            # 33 pruebas OK
python manage.py runserver
```

**Cómo verificar:** en el menú (como administrador) aparece **Reportes** con ingresos por mes, por tipo de habitación, reservaciones por estado, mejores clientes y ocupación por habitación. Cambia el periodo. Descarga el CSV y ábrelo en Excel. Inicia sesión con el usuario *Recepcionista* que creaste en la Fase 2: no debe ver Reportes ni Usuarios, y si escribe la URL `/reportes/` a mano aparece "Tu rol no tiene acceso a esta sección".

**Archivos clave:** `reportes/estadisticas.py` (todas las consultas, comentadas una por una), `reportes/views.py` (vista del reporte y exportación CSV), `cuentas/management/commands/crear_roles.py`.

**Commits**

```powershell
git add cuentas/management/
git commit -m "feat(cuentas): comando crear_roles con permisos por rol"

git add reportes/ hotel_paradise/
git commit -m "feat(reportes): estadísticas con aggregate/annotate y exportación CSV"

git add cuentas/tests.py reportes/tests.py
git commit -m "test: pruebas de login, roles y reportes"
```

## Fase 7 — Integrante 4: dashboard final y datos de demostración

**Rama:** `feature/dashboard` · **Paquete:** `fase7_integrante4_dashboard`

**Qué aprendes:** reutilizar estadísticas de otro módulo (`reportes.estadisticas`), `Count` con `filter=`, armar un tablero visual a partir de datos, comandos que generan datos de prueba (incluidas imágenes con Pillow).

El paquete reemplaza la página de inicio provisional (`core/views.py` y `core/templates/core/dashboard.html`) por el dashboard final.

```powershell
python manage.py migrate
python manage.py cargar_demo     # 14 habitaciones con foto, 22 clientes, ~740 reservaciones y 2 usuarios
python manage.py test            # 35 pruebas OK
python manage.py runserver
```

**Cómo verificar:** inicia sesión con `admin` / `Paradise2026!`. El dashboard muestra los 5 indicadores del PIA (**Total de Clientes, Total de Habitaciones, Total de Reservaciones, Habitaciones Disponibles, Ingresos Generados**), el tablero con el estado de cada habitación hoy, llegadas, salidas, próximas reservaciones y la gráfica de ingresos. Achica la ventana del navegador o ábrelo en el celular: el menú se vuelve un botón **Menú** (diseño responsivo).

`cargar_demo --reiniciar` borra habitaciones, clientes y reservaciones y vuelve a cargar todo. Úsalo antes de grabar el video.

**Commits**

```powershell
git add core/views.py core/templates/
git commit -m "feat(core): dashboard con indicadores, tablero de habitaciones y gráfica"

git add core/management/
git commit -m "feat(core): comando cargar_demo con datos de ejemplo"

git add core/tests.py
git commit -m "test(core): pruebas del dashboard"

git add README.md
git commit -m "docs: README con instrucciones de instalación"
```

Después del merge, el contenido de `main` es idéntico a `proyecto_completo/`. Pueden comprobarlo comparando carpetas.

## Fase 8 — Todos: documentación, capturas y conclusiones

**Rama:** cada quien la suya, `docs/integranteN` · **Paquete:** `fase8_todos_documentacion`

El paquete trae la carpeta `docs/` con el **Documento Técnico**, el **Manual de Usuario**, los diagramas, las capturas y una plantilla de conclusión por integrante. El orden recomendado:

1. **Integrante 4** crea la rama `docs/documentacion`, copia la carpeta `docs/` del paquete al repo y sube todo **menos** las conclusiones:

```powershell
git checkout main
git pull
git checkout -b docs/documentacion
Copy-Item -Recurse -Force "RUTA\paquetes_por_fase\fase8_todos_documentacion\*" .
git add docs/img docs/Documento_Tecnico.docx docs/Documento_Tecnico.md docs/Manual_Usuario.docx docs/Manual_Usuario.md docs/GUIA_EQUIPO.md
git commit -m "docs: documento técnico, manual de usuario, diagramas y capturas"
git push -u origin docs/documentacion
# Pull Request → revisión → Merge
```

2. **Cada integrante**, ya con eso en `main`, copia **sólo su** plantilla `docs/conclusiones/integranteN.md` del paquete, la llena con su conclusión personal (qué hizo, qué aprendió, qué le costó, qué mejoraría) y hace su propio commit:

```powershell
git checkout main
git pull
git checkout -b docs/integrante1
# copia paquetes_por_fase\fase8_todos_documentacion\docs\conclusiones\integrante1.md
# a docs\conclusiones\ y edítalo
git add docs/conclusiones/integrante1.md
git commit -m "docs: conclusión individual del Integrante 1"
git push -u origin docs/integrante1
# Pull Request → revisión → Merge
```

3. Copien las conclusiones finales a la sección 9 del Documento Técnico, pongan sus nombres en la portada y en el README (tabla "Equipo") y súbanlo en un último commit.

**Al terminar** revisen en GitHub **Insights → Contributors**: deben aparecer los 5 con commits. En **Pull requests → Closed** deben verse los PR revisados.

# 5. Cómo correr el proyecto completo (para cualquiera, en cualquier momento)

```powershell
git clone https://github.com/USUARIO/hotel-paradise.git
cd hotel-paradise
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py cargar_demo
python manage.py runserver
```

| Usuario | Contraseña | Rol |
|---|---|---|
| `admin` | `Paradise2026!` | Administrador: todo, incluyendo reportes, usuarios y Django Admin |
| `recepcion` | `Recepcion2026!` | Recepcionista: clientes y reservaciones; habitaciones sólo de consulta |

# 6. Errores comunes y cómo resolverlos

| Síntoma | Causa | Solución |
|---|---|---|
| `python` no se reconoce | No se marcó "Add to PATH" | Reinstala Python marcando la casilla, o usa `py` en lugar de `python` |
| PowerShell no deja activar `venv` | Política de ejecución | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `No module named 'django'` | No activaste el entorno virtual | `venv\Scripts\activate` (debe aparecer `(venv)` al inicio de la línea) |
| `no such table: habitaciones_habitacion` | Falta migrar | `python manage.py migrate` |
| `Cannot use ImageField because Pillow is not installed` | Falta Pillow | `pip install -r requirements.txt` |
| `NoReverseMatch` | Falta la línea `include(...)` en `urls.py` o la app en `INSTALLED_APPS` | Revisa que copiaste los archivos de `hotel_paradise/` de tu paquete |
| La página se ve sin estilos | Ruta de `static` mal | Corre el servidor desde la carpeta donde está `manage.py` |
| `CSRF verification failed` | Formulario sin `{% csrf_token %}` | Todos los formularios POST del proyecto lo traen; no lo borres |
| Error 403 "Tu rol no tiene acceso" | Usuario sin permisos | Entra como `admin`, o corre `python manage.py crear_roles` y asigna el rol |
| `git push` rechazado ("fetch first") | Alguien subió cambios antes | `git pull` y después `git push` |
| Conflicto al hacer `git pull` o merge | Dos personas cambiaron las mismas líneas | Abre el archivo en VS Code, elige *Accept Incoming* / *Accept Current* / *Accept Both*, guarda, `git add archivo` y `git commit` |
| Se subió `db.sqlite3` o `venv/` por error | Se hizo `git add .` antes del `.gitignore` | `git rm -r --cached venv db.sqlite3` y commit |

# 7. Cómo cumple el proyecto cada punto de la rúbrica

| Criterio (puntos) | Dónde se ve |
|---|---|
| Diseño correcto de modelos y relaciones (15) | 3 modelos con los campos del PIA; `Reservacion` con dos `ForeignKey` (1:N con Cliente y con Habitación); diagrama E-R en el Documento Técnico |
| CRUD de Habitaciones (10) | Crear, consultar, modificar, eliminar con foto; búsqueda por número y tipo |
| CRUD de Clientes (10) | Crear, consultar, modificar, eliminar; búsqueda por nombre, correo o teléfono |
| CRUD de Reservaciones (15) | Crear, consultar, modificar y **cancelar**; búsqueda por cliente, habitación, tipo y estado |
| Validación de disponibilidad (10) | `Reservacion.clean()` (Regla 1) y pantalla *Consultar disponibilidad* |
| Formularios y validaciones (10) | Reglas 1–5, teléfono de 10 dígitos, capacidad, fechas pasadas, tamaño de imagen, mensajes en español con campos en rojo |
| Interfaz gráfica Bootstrap (10) | Bootstrap 5 local, diseño propio, responsivo con menú desplegable en celular |
| Dashboard y estadísticas (5) | Los 5 indicadores + tablero + gráfica; módulo de Reportes con 5 estadísticas y CSV |
| Git/GitHub y participación (5) | Commits de los 5 integrantes, ramas por módulo y Pull Requests revisados |
| Documentación técnica y manual (5) | `docs/Documento_Tecnico.docx` y `docs/Manual_Usuario.docx` |
| Presentación y demostración (5) | Video de 5 minutos con el guion de la sección 8 |

Extras que suman a la calidad: 35 pruebas automáticas, roles con permisos, Django Admin personalizado, exportación a CSV, impresión de comprobantes, páginas 403/404 propias y datos de demostración.

# 8. Guion del video (5 minutos, 1 minuto por integrante)

Hay una presentación de apoyo de 14 diapositivas (link en el chat donde recibieron este material) con el guion de cada integrante en las notas del orador; se puede presentar desde el navegador o descargar como PowerPoint o PDF.

Antes de grabar: `python manage.py cargar_demo --reiniciar`, navegador en pantalla completa, zoom al 100 %. Graben con OBS, la grabación de Teams/Zoom o la Barra de juegos de Windows (`Win + G`). Cada quien puede grabar su minuto por separado y se unen al final (Clipchamp, CapCut o el editor de fotos de Windows).

| Tiempo | Quién | Qué muestra en pantalla | Qué dice (idea, no lo lean) |
|---|---|---|---|
| 0:00–1:00 | **Integrante 4** | Login → dashboard → tablero de habitaciones → achicar ventana para mostrar el menú móvil | Presenta el equipo y el problema del hotel. Explica el flujo Usuario → URL → Vista → Formulario → Modelo → BD → Template. Muestra la plantilla base, Bootstrap y los 5 indicadores del dashboard. |
| 1:00–2:00 | **Integrante 1** | Habitaciones → nueva con foto → número repetido (Regla 3) → filtro por tipo → Django Admin | Explica el modelo `Habitacion`, `unique=True`, `ImageField` y las vistas genéricas del CRUD. |
| 2:00–3:00 | **Integrante 2** | Clientes → nuevo → correo repetido en mayúsculas (Regla 4) → teléfono inválido → búsqueda | Explica `EmailField`, la validación `clean_correo` y la búsqueda con `Q`. |
| 3:00–4:00 | **Integrante 3** | Disponibilidad → reservar → total automático → traslape (Regla 1) → salida antes de entrada (Regla 2) → intentar eliminar la habitación (Regla 5) → cancelar | Explica las dos `ForeignKey` (relación 1 a N), la fórmula de traslape y el `CheckConstraint`. |
| 4:00–5:00 | **Integrante 5** | Cerrar sesión → entrar como recepcionista (menú reducido, 403 en reportes) → entrar como admin → Reportes → CSV → Usuarios | Explica login/logout, roles con grupos y permisos, y las consultas `aggregate`/`annotate` de los reportes. Cierra con lo aprendido y el repositorio en GitHub (Insights → Contributors). |

# 9. Preguntas que les pueden hacer (y la respuesta corta)

**Integrante 1 — Habitaciones**

- *¿Cómo evitan números repetidos?* Con `unique=True` en el campo `numero`: Django crea un índice único en la tabla y el `ModelForm` muestra el error antes de guardar.
- *¿Dónde se guardan las fotos?* En la carpeta `media/habitaciones/`; la base de datos sólo guarda la ruta. `MEDIA_ROOT` y `MEDIA_URL` están en `settings.py`.
- *¿Por qué no se borra una habitación con reservaciones?* Regla 5: `form_valid` del `DeleteView` revisa `tiene_reservaciones_activas()` y, si hay, regresa con un mensaje en lugar de borrar.

**Integrante 2 — Clientes**

- *¿Qué pasa si escriben el mismo correo con mayúsculas?* `clean_correo` lo pasa a minúsculas y busca con `correo__iexact`, que ignora mayúsculas; además `save()` siempre guarda en minúsculas.
- *¿Cómo funciona la búsqueda?* Se separa el texto en palabras y cada una se busca con `Q(nombre__icontains) | Q(apellidos__icontains) | ...`; `|` significa "o".
- *¿Qué es `auto_now_add`?* Django pone la fecha y hora automáticamente al crear el registro.

**Integrante 3 — Reservaciones**

- *¿Qué es una relación uno a muchos?* Un cliente puede tener muchas reservaciones, pero cada reservación es de un solo cliente; se implementa con `ForeignKey` en `Reservacion`.
- *¿Cómo detectan que dos reservaciones chocan?* `entrada_existente < salida_nueva` y `salida_existente > entrada_nueva`, sólo entre reservaciones activas de la misma habitación.
- *¿Por qué se cancela en lugar de borrar?* Para conservar el historial y los reportes; una cancelada ya no ocupa la habitación.

**Integrante 4 — Interfaz y dashboard**

- *¿Qué es `{% extends %}`?* Herencia de plantillas: `base.html` tiene el menú y cada página sólo llena el bloque `contenido`.
- *¿Cómo calculan "habitaciones disponibles"?* Habitaciones en servicio que no tienen una reservación activa que cubra el día de hoy.
- *¿Por qué Bootstrap está en `static/` y no por CDN?* Para que el sistema funcione aunque no haya internet en la presentación.

**Integrante 5 — Seguridad y reportes**

- *¿Por qué el logout es un formulario y no un enlace?* Desde Django 5 el logout requiere POST con token CSRF, para que otra página no pueda cerrarte la sesión con un simple enlace.
- *¿Cómo funcionan los roles?* Son grupos de Django con permisos (`view`, `add`, `change`, `delete`); las vistas piden un permiso con `permission_required`.
- *¿Qué diferencia hay entre `aggregate` y `annotate`?* `aggregate` da un solo resultado para toda la consulta (ingreso total); `annotate` da un resultado por grupo (ingreso por mes).
