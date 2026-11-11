# 1. Objetivo

## 1.1 Objetivo general

Desarrollar una aplicación web completa con el framework Django para administrar las reservaciones de la cadena Hotel Paradise, mediante un sistema multiusuario que controle habitaciones, clientes y reservas, valide automáticamente la disponibilidad y genere estadísticas para la toma de decisiones.

## 1.2 Objetivos específicos

1. Diseñar una base de datos relacional en SQLite con tres entidades (Cliente, Habitación y Reservación) y dos relaciones uno a muchos.
2. Implementar el CRUD completo de habitaciones, clientes y reservaciones con formularios validados.
3. Garantizar por código las cinco reglas de negocio del hotel, en especial que una habitación no se reserve dos veces en las mismas fechas.
4. Construir una interfaz responsiva con Bootstrap 5 que funcione en computadora y en celular.
5. Proteger el sistema con inicio de sesión, cierre de sesión y roles con permisos diferenciados.
6. Ofrecer un dashboard y reportes con consultas avanzadas del ORM de Django.
7. Trabajar de forma colaborativa con Git y GitHub, con commits individuales por integrante.
8. Comprobar el funcionamiento con pruebas automáticas.

# 2. Descripción del problema

Hotel Paradise es una cadena hotelera que maneja cuatro tipos de habitación: **Individual, Doble, Suite y Presidencial**. Hasta ahora el personal de recepción controlaba la ocupación en hojas de cálculo y libretas, lo que provocaba tres problemas recurrentes:

- **Sobreventa:** dos recepcionistas podían prometer la misma habitación para fechas que se traslapaban, porque no había una fuente única y actualizada de disponibilidad.
- **Datos de clientes duplicados o incompletos:** un mismo huésped quedaba registrado varias veces con correos escritos de forma distinta, y faltaban teléfonos válidos para confirmar estancias.
- **Falta de información para decidir:** la gerencia no sabía con rapidez cuántas habitaciones estaban libres hoy, cuánto se había facturado en el mes o qué tipo de habitación generaba más ingresos.

El hotel necesita una aplicación web, accesible para el personal desde cualquier navegador, que permita consultar disponibilidad, registrar clientes, hacer y cancelar reservaciones con el total calculado automáticamente y consultar reportes básicos, todo con control de acceso por usuario.

## 2.1 Requerimientos funcionales

| Módulo | Requerimiento |
|---|---|
| Habitaciones | Registrar número, tipo, precio por noche, capacidad, disponibilidad e imagen. CRUD completo y búsqueda por número y por tipo. |
| Clientes | Registrar nombre, apellidos, correo, teléfono y fecha de registro automática. CRUD completo y búsqueda por cliente. |
| Reservaciones | Registrar cliente, habitación, fecha de entrada, fecha de salida, total y estado. Crear, consultar, modificar y cancelar. Búsqueda por cliente, habitación y tipo de habitación. |
| Dashboard | Mostrar total de clientes, total de habitaciones, total de reservaciones, habitaciones disponibles e ingresos generados. |
| Seguridad | Login, logout y control de usuarios. |
| Reportes | Estadísticas de ingresos y ocupación. |

## 2.2 Reglas de negocio

| Regla | Descripción | Implementación |
|---|---|---|
| 1 | Una habitación no podrá reservarse dos veces en las mismas fechas. | `Reservacion.clean()` busca reservaciones activas que se traslapen antes de guardar. |
| 2 | La fecha de salida debe ser mayor que la fecha de entrada. | `Reservacion.clean()` y una restricción `CheckConstraint` en la base de datos. |
| 3 | No se pueden registrar habitaciones con números repetidos. | `unique=True` en `Habitacion.numero`, con mensaje propio. |
| 4 | El correo del cliente debe ser único. | `unique=True` en `Cliente.correo` y `ClienteForm.clean_correo()` que ignora mayúsculas. |
| 5 | No se puede eliminar una habitación con reservaciones activas. | `HabitacionDeleteView.form_valid()` y `HabitacionAdmin.has_delete_permission()`. |

# 3. Diagrama Entidad-Relación

El modelo relacional respeta el esquema solicitado en el PIA. La entidad **Reservación** es la tabla intermedia que relaciona a un **Cliente** con una **Habitación**; ambas relaciones son de uno a muchos: un cliente puede tener muchas reservaciones a lo largo del tiempo y una habitación puede recibir muchas reservaciones, pero cada reservación pertenece a un solo cliente y a una sola habitación.

![Diagrama Entidad-Relación de Hotel Paradise](img/er.png "|6.3")

## 3.1 Diccionario de datos

**Tabla `clientes_cliente`** (modelo `Cliente`, app `clientes`)

| Campo | Tipo Django | Tipo SQL | Restricciones |
|---|---|---|---|
| id | BigAutoField | integer | Llave primaria |
| nombre | CharField(80) | varchar(80) | Obligatorio, sin números |
| apellidos | CharField(120) | varchar(120) | Obligatorio, sin números |
| correo | EmailField | varchar(254) | Obligatorio, **único**, formato de correo |
| telefono | CharField(10) | varchar(10) | Obligatorio, exactamente 10 dígitos |
| fecha_registro | DateTimeField(auto_now_add) | datetime | Automática al crear |

**Tabla `habitaciones_habitacion`** (modelo `Habitacion`, app `habitaciones`)

| Campo | Tipo Django | Tipo SQL | Restricciones |
|---|---|---|---|
| id | BigAutoField | integer | Llave primaria |
| numero | PositiveIntegerField | integer unsigned | Obligatorio, **único**, mínimo 1 |
| tipo | CharField(20, choices) | varchar(20) | INDIVIDUAL, DOBLE, SUITE o PRESIDENCIAL |
| precio_noche | DecimalField(10, 2) | decimal | Mínimo 1.00 |
| capacidad | PositiveSmallIntegerField | smallint unsigned | De 1 a 10 personas |
| disponible | BooleanField | bool | Por defecto verdadero |
| imagen | ImageField | varchar(100) | Opcional, máximo 2 MB, se guarda en `media/habitaciones/` |
| descripcion | TextField | text | Opcional |

**Tabla `reservaciones_reservacion`** (modelo `Reservacion`, app `reservaciones`)

| Campo | Tipo Django | Tipo SQL | Restricciones |
|---|---|---|---|
| id | BigAutoField | integer | Llave primaria |
| cliente_id | ForeignKey(Cliente) | bigint | Llave foránea, `related_name="reservaciones"` |
| habitacion_id | ForeignKey(Habitacion) | bigint | Llave foránea, `related_name="reservaciones"` |
| fecha_entrada | DateField | date | Obligatoria, no anterior a hoy al crear |
| fecha_salida | DateField | date | Obligatoria, mayor que la entrada (CHECK) |
| num_huespedes | PositiveSmallIntegerField | smallint | Mínimo 1, no mayor a la capacidad |
| total | DecimalField(12, 2) | decimal | Calculado: noches × precio por noche |
| estado | CharField(12, choices) | varchar(12) | PENDIENTE, CONFIRMADA, FINALIZADA o CANCELADA |
| notas | TextField | text | Opcional |
| creada / actualizada | DateTimeField | datetime | Automáticas |

Además del esquema mínimo del PIA se agregaron `num_huespedes` (para validar la capacidad), `notas`, `descripcion` y las fechas de auditoría, que no alteran las relaciones pedidas.

# 4. Arquitectura del proyecto

## 4.1 Patrón MTV de Django

Django sigue el patrón **Modelo – Template – Vista (MTV)**, la variante de Django del patrón MVC. Cada petición del navegador recorre el flujo que pide el PIA: Usuario → URL → Vista → Formulario → Modelo → Base de datos → Template → Navegador.

![Flujo de una petición en Hotel Paradise](img/arq.png "|6.5")

| Capa | Responsabilidad en el proyecto |
|---|---|
| **URLs** (`urls.py`) | El archivo principal incluye las rutas de cada app con un prefijo (`/habitaciones/`, `/clientes/`…). Cada app tiene su `app_name` para usar nombres como `habitaciones:lista`. |
| **Vistas** (`views.py`) | Vistas genéricas basadas en clases (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`) y vistas de función para cancelar y consultar disponibilidad. Revisan sesión y permisos. |
| **Formularios** (`forms.py`) | `ModelForm` con validaciones por campo (`clean_correo`, `clean_capacidad`) y formularios de búsqueda. Todos heredan `BootstrapFormMixin` para el estilo. |
| **Modelos** (`models.py`) | Definen tablas, relaciones y reglas de negocio (`clean()`, `save()`, métodos como `tiene_reservaciones_activas()`). |
| **Base de datos** | SQLite (`db.sqlite3`) creada con migraciones. |
| **Templates** | HTML con el lenguaje de plantillas de Django y Bootstrap 5. Todas heredan de `templates/base.html`. |

## 4.2 Organización en apps

El proyecto se dividió en seis apps, una por responsabilidad, lo que permitió que cada integrante trabajara en su carpeta sin interferir con los demás.

![Apps del proyecto y sus dependencias](img/modulos.png "|5.6")

```
hotel-paradise/
├── manage.py
├── requirements.txt            Django 5.2 y Pillow
├── hotel_paradise/             configuración del proyecto
│   ├── settings.py
│   └── urls.py
├── core/                       dashboard, mixins, formularios base, cargar_demo
├── cuentas/                    login, logout, roles, usuarios, crear_roles
├── habitaciones/               modelo Habitacion, CRUD, admin
├── clientes/                   modelo Cliente, CRUD, admin
├── reservaciones/              modelo Reservacion, CRUD, disponibilidad
├── reportes/                   estadísticas (ORM) y exportación CSV
├── templates/                  base.html, parciales, 403.html, 404.html
├── static/                     css/hotel.css, js/graficas.js, vendor/ (Bootstrap, íconos, Chart.js, fuentes)
├── media/                      fotografías subidas (no se versiona)
└── docs/                       documentación
```

## 4.3 Tecnologías

| Tecnología | Versión | Uso |
|---|---|---|
| Python | 3.12 / 3.13 | Lenguaje del backend |
| Django | 5.2 LTS | Framework web: ORM, formularios, autenticación, admin |
| SQLite | 3 | Base de datos (requerimiento técnico) |
| Pillow | 10 o superior | Manejo de las fotografías de habitaciones (`ImageField`) |
| Bootstrap | 5.3.8 | Componentes y rejilla responsiva (guardado en `static/`) |
| Bootstrap Icons | 1.13 | Íconos de la interfaz |
| Chart.js | 4.6 | Gráficas del dashboard y de reportes |
| Git y GitHub | — | Control de versiones y trabajo colaborativo |

Bootstrap, los íconos, Chart.js y las tipografías se guardaron en la carpeta `static/vendor/` en lugar de cargarse desde internet: así el sistema se ve igual aunque no haya conexión durante la presentación.

## 4.4 Seguridad y roles

| Mecanismo | Descripción |
|---|---|
| Autenticación | `LoginView` y `LogoutView` de `django.contrib.auth` con plantillas propias. El logout se hace por POST con token CSRF. |
| Sesión obligatoria | Todas las vistas usan `PermisoRequeridoMixin` o `login_required`: quien no ha iniciado sesión es enviado al login. |
| Permisos | Cada vista declara `permission_required` (por ejemplo `habitaciones.add_habitacion`). Sin permiso se muestra la página 403. |
| CSRF | Todos los formularios POST incluyen `{% csrf_token %}`. |
| Contraseñas | Guardadas con hash PBKDF2 y validadas con los validadores de Django. |

| Permiso | Administrador | Recepcionista |
|---|---|---|
| Habitaciones | Consultar, crear, modificar, eliminar | Sólo consultar |
| Clientes | Consultar, crear, modificar, eliminar | Consultar, crear, modificar |
| Reservaciones | Consultar, crear, modificar, cancelar | Consultar, crear, modificar, cancelar |
| Reportes y usuarios | Sí | No |
| Django Admin | Sí | No |

Los roles son grupos de Django creados con el comando `python manage.py crear_roles`.

## 4.5 Mapa de URLs

| URL | Vista | Descripción |
|---|---|---|
| `/` | `DashboardView` | Dashboard principal |
| `/cuentas/login/` · `/cuentas/logout/` | `LoginView` · `LogoutView` | Iniciar y cerrar sesión |
| `/cuentas/usuarios/` | `UsuarioListView` | Control de usuarios (alta y edición) |
| `/habitaciones/` | `HabitacionListView` | Lista y búsqueda; `nueva/`, `<id>/`, `<id>/editar/`, `<id>/eliminar/` |
| `/clientes/` | `ClienteListView` | Lista y búsqueda; `nuevo/`, `<id>/`, `<id>/editar/`, `<id>/eliminar/` |
| `/reservaciones/` | `ReservacionListView` | Lista y búsqueda; `nueva/`, `<id>/`, `<id>/editar/`, `<id>/cancelar/` |
| `/reservaciones/disponibilidad/` | `disponibilidad` | Consulta de habitaciones libres por fechas |
| `/reportes/` · `/reportes/exportar/` | `ReporteView` · `ExportarCSVView` | Estadísticas y descarga CSV |
| `/admin/` | Django Admin | Panel administrativo |

# 5. Explicación de módulos

## 5.1 Módulo Habitaciones (Integrante 1)

**Archivos:** `habitaciones/models.py`, `forms.py`, `views.py`, `urls.py`, `admin.py`, `templates/habitaciones/`, `tests.py`.

El modelo `Habitacion` define los cuatro tipos con `choices`, lo que limita los valores posibles y genera automáticamente la lista desplegable del formulario. El número de habitación tiene `unique=True` (Regla 3) y la fotografía se maneja con `ImageField`, que guarda el archivo en `media/habitaciones/` y sólo la ruta en la base de datos. El formulario valida además que la capacidad no supere 10 personas y que la imagen no pese más de 2 MB.

El CRUD usa las vistas genéricas de Django. La lista muestra tarjetas con foto, precio y estado, y permite buscar por número o descripción y filtrar por tipo y por estado. La Regla 5 se aplica al confirmar el borrado:

```python
def form_valid(self, form):
    # Regla 5: no se puede eliminar una habitación con reservaciones activas.
    if self.object.tiene_reservaciones_activas():
        messages.error(self.request, "No se puede eliminar ...: tiene reservaciones activas.")
        return redirect(self.object.get_absolute_url())
    return super().form_valid(form)
```

En el **panel administrativo** (`/admin/`) las habitaciones se muestran con miniatura de la foto, filtros por tipo y disponibilidad, edición rápida del precio y acciones para marcar varias habitaciones como disponibles o fuera de servicio. La misma Regla 5 bloquea el borrado desde el admin.

## 5.2 Módulo Clientes (Integrante 2)

**Archivos:** `clientes/models.py`, `forms.py`, `views.py`, `urls.py`, `admin.py`, `templates/clientes/`, `tests.py`.

El modelo `Cliente` guarda la fecha de registro de forma automática con `auto_now_add=True` y valida el teléfono con un `RegexValidator` de 10 dígitos. Para cumplir la Regla 4 sin importar cómo escriba el usuario el correo, el método `save()` lo convierte a minúsculas y el formulario lo compara con `correo__iexact`:

```python
def clean_correo(self):
    correo = self.cleaned_data["correo"].strip().lower()
    repetido = Cliente.objects.filter(correo__iexact=correo)
    if self.instance.pk:                      # al editar se excluye al propio cliente
        repetido = repetido.exclude(pk=self.instance.pk)
    if repetido.exists():
        raise forms.ValidationError("Ya existe un cliente registrado con este correo.")
    return correo
```

La búsqueda separa el texto en palabras y busca cada una en nombre, apellidos, correo o teléfono con objetos `Q` unidos con `|` (OR). El detalle del cliente muestra su historial de reservaciones gracias al `related_name="reservaciones"` de la llave foránea.

## 5.3 Módulo Reservaciones (Integrante 3)

**Archivos:** `reservaciones/models.py`, `forms.py`, `views.py`, `urls.py`, `admin.py`, `templates/reservaciones/`, `tests.py`.

El modelo `Reservacion` contiene las dos llaves foráneas que forman las relaciones uno a muchos y un estado con `TextChoices`. Las validaciones viven en `clean()`, que Django ejecuta automáticamente cuando se llama `form.is_valid()` en un `ModelForm`. Dos estancias chocan si la entrada existente es anterior a la nueva salida **y** la salida existente es posterior a la nueva entrada; así, el día de salida de un huésped puede ser el día de entrada del siguiente:

```python
qs = Reservacion.objects.filter(
    habitacion=habitacion,
    estado__in=[Estado.PENDIENTE, Estado.CONFIRMADA],   # las canceladas no ocupan
    fecha_entrada__lt=salida,
    fecha_salida__gt=entrada,
).exclude(pk=self.pk)                                    # al editar, no chocar consigo misma
```

`clean()` también valida que la salida sea mayor que la entrada (Regla 2), que no se reserve en fechas pasadas, que la habitación esté en servicio y que el número de huéspedes no supere la capacidad. Como segunda línea de defensa, la Regla 2 está declarada en la base de datos con un `CheckConstraint`. El método `save()` calcula el total como noches × precio por noche, así que el usuario nunca lo escribe a mano.

Las reservaciones no se eliminan: se **cancelan** (cambio de estado), para conservar el historial y que los reportes sean correctos. La pantalla **Consultar disponibilidad** recibe fechas, tipo y número de huéspedes y muestra sólo las habitaciones libres usando una subconsulta: `Habitacion.objects.exclude(pk__in=ocupadas)`. Desde cada resultado se llega al formulario de reservación con los datos ya llenos.

## 5.4 Interfaz web y dashboard (Integrante 4)

**Archivos:** `templates/base.html`, `templates/partials/`, `static/css/hotel.css`, `static/js/graficas.js`, `core/`.

Todas las páginas heredan de `base.html`, que contiene el menú lateral, la barra superior con el usuario y el botón de cerrar sesión, y el área de mensajes. En pantallas pequeñas el menú se convierte en un panel desplegable (*offcanvas* de Bootstrap). El menú sólo muestra las secciones que el rol del usuario puede usar, consultando `perms` en la plantilla.

El diseño usa una paleta índigo con verde laguna para "libre", ámbar para "pendiente" y coral para "cancelada", aplicada de forma consistente en etiquetas de estado, botones y gráficas. Los parciales `campo.html`, `paginacion.html` y `errores_formulario.html` evitan repetir código en los formularios y listas.

El **dashboard** muestra los cinco indicadores pedidos (total de clientes, habitaciones, reservaciones, habitaciones disponibles hoy e ingresos generados), un tablero con el estado de cada habitación en el día, las llegadas, salidas y próximas reservaciones y una gráfica de ingresos de los últimos seis meses. "Habitaciones disponibles" se calcula como las habitaciones en servicio que no tienen una reservación activa que cubra el día de hoy.

## 5.5 Seguridad y reportes (Integrante 5)

**Archivos:** `cuentas/` y `reportes/`.

La app `cuentas` personaliza el login y el logout de Django, define los roles Administrador y Recepcionista (`permisos.py`), ofrece pantallas para dar de alta usuarios, cambiar su rol o desactivarlos, y el comando `crear_roles` que asigna los permisos a cada grupo.

La app `reportes` concentra las consultas avanzadas del ORM en `estadisticas.py`, que también reutiliza el dashboard. Por ejemplo, los ingresos por mes se obtienen agrupando con `TruncMonth`, `values()` y `annotate()`, lo que Django traduce a un `GROUP BY`:

```python
(Reservacion.objects
    .filter(estado__in=["CONFIRMADA", "FINALIZADA"], fecha_entrada__range=(desde, hasta))
    .annotate(mes=TruncMonth("fecha_entrada"))
    .values("mes")
    .annotate(ingresos=Sum("total"), reservas=Count("id"))
    .order_by("mes"))
```

El reporte permite elegir el periodo y muestra: número de reservaciones y canceladas, ticket promedio, porcentaje de ocupación, ingresos por mes y por tipo de habitación, reservaciones por estado, los cinco clientes con mayor consumo y la ocupación de cada habitación. Se puede imprimir o exportar a CSV para abrirlo en Excel.

# 6. Capturas del sistema

![Pantalla de inicio de sesión](img/capturas/01_login.png)

![Dashboard principal con los cinco indicadores y el tablero de habitaciones](img/capturas/03_dashboard.png "|5.2")

![Lista de habitaciones con fotografía, búsqueda y filtros](img/capturas/04_habitaciones_lista.png "|5.2")

![Validación de la Regla 3: número de habitación repetido](img/capturas/07_habitacion_numero_repetido.png)

![Validación de la Regla 5: la habitación tiene reservaciones activas](img/capturas/09_habitacion_regla5.png)

![Lista y búsqueda de clientes](img/capturas/11_clientes_lista.png "|5.6")

![Validaciones de correo único (Regla 4) y teléfono](img/capturas/13_cliente_validaciones.png)

![Consulta de disponibilidad por fechas](img/capturas/17_disponibilidad.png "|5.6")

![Registro de reservación con el total estimado](img/capturas/18_reservacion_nueva.png)

![Validación de la Regla 1: la habitación ya está reservada en esas fechas](img/capturas/20_regla1_traslape.png)

![Validación de la Regla 2: la salida debe ser posterior a la entrada](img/capturas/21_regla2_fechas.png)

![Cancelación de una reservación](img/capturas/23_reservacion_cancelar.png)

![Módulo de reportes y estadísticas](img/capturas/25_reportes.png "|4.6")

![Control de usuarios](img/capturas/26_usuarios.png)

![Panel administrativo de Django](img/capturas/29_admin_habitaciones.png)

![Menú reducido del rol Recepcionista](img/capturas/30_dashboard_recepcion.png)

![Diseño responsivo en celular](img/capturas/33_movil_menu.png "|2.6")

# 7. Pruebas funcionales

Se escribieron **35 pruebas automáticas** con el módulo `django.test`. Cada prueba crea una base de datos temporal, ejecuta la acción y compara el resultado esperado. Se corren con `python manage.py test` y todas pasan.

| Módulo | Prueba | Qué comprueba |
|---|---|---|
| Habitaciones | `test_crear_habitacion_desde_la_vista` | El formulario registra una habitación |
| Habitaciones | `test_regla3_numero_repetido` | No se acepta un número existente |
| Habitaciones | `test_capacidad_maxima` | No se acepta capacidad mayor a 10 |
| Habitaciones | `test_busqueda_por_tipo` | El filtro por tipo muestra sólo ese tipo |
| Habitaciones | `test_modificar_y_eliminar` | Se edita el precio y se elimina sin reservaciones |
| Habitaciones | `test_requiere_iniciar_sesion` | Sin sesión, redirige al login |
| Clientes | `test_crear_cliente` | El formulario registra un cliente |
| Clientes | `test_regla4_correo_unico_sin_importar_mayusculas` | Rechaza el mismo correo en mayúsculas |
| Clientes | `test_correo_invalido` / `test_telefono_10_digitos` | Formato de correo y teléfono |
| Clientes | `test_editar_conserva_su_propio_correo` | Al editar no choca consigo mismo |
| Clientes | `test_busqueda` / `test_eliminar` | Búsqueda por apellido y borrado |
| Reservaciones | `test_total_se_calcula_solo` | 3 noches × $1,000 = $3,000 |
| Reservaciones | `test_regla1_no_se_traslapan` | Rechaza fechas que se traslapan |
| Reservaciones | `test_salida_de_uno_es_entrada_del_siguiente` | Permite entrar el día que otro sale |
| Reservaciones | `test_regla2_salida_mayor_que_entrada` | Rechaza salida igual o anterior a la entrada |
| Reservaciones | `test_cancelada_libera_la_habitacion` | Una cancelada no bloquea fechas |
| Reservaciones | `test_capacidad` / `test_no_fechas_pasadas` | Capacidad y fechas pasadas |
| Reservaciones | `test_cancelar_desde_la_vista` | Cancelar cambia el estado |
| Reservaciones | `test_disponibilidad_excluye_ocupadas` | La consulta no muestra habitaciones ocupadas |
| Reservaciones | `test_regla5_no_eliminar_habitacion_con_reservaciones_activas` | La habitación reservada no se borra |
| Reservaciones | `test_crear_desde_la_vista` | El formulario registra la reservación |
| Cuentas | `test_login_correcto` / `test_login_incorrecto` / `test_logout` | Inicio y cierre de sesión |
| Cuentas | `test_recepcionista_no_puede_crear_habitaciones` | El rol limita el acceso (403) |
| Cuentas | `test_recepcionista_no_ve_usuarios` / `test_admin_crea_usuario` | Control de usuarios |
| Reportes | `test_ingresos_excluyen_canceladas` / `test_resumen` | Cálculo de ingresos y resumen |
| Reportes | `test_vista_reporte_y_csv` | El reporte y el CSV se generan |
| Dashboard | `test_indicadores` / `test_requiere_sesion` | Los cinco indicadores y el acceso |

## 7.1 Evidencias de funcionamiento

| Evidencia solicitada | Dónde se muestra |
|---|---|
| Login | Figura 4 |
| Menú principal | Figuras 5 y 19 (administrador y recepcionista) |
| CRUD Habitaciones | Figuras 6, 7, 8 y 18 |
| CRUD Clientes | Figuras 9 y 10 |
| CRUD Reservaciones | Figuras 12 y 15 |
| Validación de fechas | Figura 14 |
| Validación de disponibilidad | Figuras 11 y 13 |
| Dashboard | Figura 5 |

# 8. Control de versiones

El código se administró en un repositorio de GitHub con una rama `main` protegida. Cada integrante trabajó en una rama propia (`feature/habitaciones`, `feature/clientes`, etc.) y la integró a `main` mediante un Pull Request revisado por otro compañero. Los módulos se integraron en orden de dependencia para que el sistema funcionara al final de cada fase.

| Fase | Integrante | Rama | Commits principales |
|---|---|---|---|
| 1 | Integrante 4 | `main` | Proyecto base; app core; plantilla base y estilos |
| 2 | Integrante 5 | `feature/cuentas` | Login y logout; control de usuarios |
| 3 | Integrante 1 | `feature/habitaciones` | Modelo (Regla 3); admin; CRUD (Regla 5); pruebas |
| 4 | Integrante 2 | `feature/clientes` | Modelo (Regla 4); CRUD y búsqueda; pruebas |
| 5 | Integrante 3 | `feature/reservaciones` | Modelo (Reglas 1 y 2); registrar/modificar/cancelar; pruebas |
| 6 | Integrante 5 | `feature/reportes` | Comando de roles; estadísticas y CSV; pruebas |
| 7 | Integrante 4 | `feature/dashboard` | Dashboard; datos de demostración; pruebas; README |
| 8 | Todos | `docs/integranteN` | Documentación y conclusiones individuales |

Repositorio: **https://github.com/[usuario]/hotel-paradise**

# 9. Conclusiones individuales

> Cada integrante sustituye el texto de su apartado por su propia conclusión (qué hizo, qué aprendió, qué se le dificultó y qué mejoraría). Los párrafos siguientes son sólo un punto de partida.

## Integrante 1 — Módulo Habitaciones

Desarrollar el módulo de habitaciones me permitió entender cómo un modelo de Django se convierte en una tabla mediante las migraciones y cómo las restricciones como `unique=True` protegen los datos desde la base de datos. Lo más retador fue el manejo de imágenes, porque implica configurar `MEDIA_ROOT`, usar `enctype="multipart/form-data"` en el formulario y validar el tamaño del archivo. También comprendí el valor de las vistas genéricas: con pocas líneas se obtiene un CRUD completo. Como mejora, agregaría varias fotografías por habitación y un calendario visual de ocupación.

## Integrante 2 — Módulo Clientes

En el módulo de clientes aprendí que validar un dato no es sólo revisar su formato: el correo `Ana@correo.com` y `ana@correo.com` son el mismo, así que fue necesario normalizarlo y comparar sin distinguir mayúsculas. También practiqué los validadores con expresiones regulares y las búsquedas con objetos `Q` para consultar varios campos a la vez. Me di cuenta de lo importante que es dar mensajes de error claros al usuario. Como mejora, agregaría la exportación del directorio de clientes y la detección de posibles duplicados por nombre.

## Integrante 3 — Módulo Reservaciones

El módulo de reservaciones fue el centro del sistema, porque une a clientes y habitaciones mediante dos llaves foráneas. La parte más importante fue diseñar la validación de traslapes: entender que dos rangos de fechas chocan cuando uno empieza antes de que el otro termine me permitió resolver la Regla 1 con una sola consulta. Aprendí a poner las reglas de negocio en el método `clean()` del modelo para que se apliquen en cualquier formulario, y a proteger la Regla 2 también en la base de datos. Como mejora, agregaría pagos y anticipos y el envío de la confirmación por correo.

## Integrante 4 — Interfaz web y dashboard

Mi responsabilidad fue la estructura del proyecto y la interfaz. Aprendí a usar la herencia de plantillas para que todo el sistema comparta el mismo menú y estilo, a integrar Bootstrap 5 de forma local y a adaptar el diseño a celulares. Construir el dashboard me obligó a entender los datos de todos los módulos y a reutilizar las consultas del módulo de reportes. También coordiné el repositorio y el orden de integración, lo que me enseñó la importancia de acordar convenciones desde el principio. Como mejora, agregaría un modo oscuro y actualización automática del tablero.

## Integrante 5 — Seguridad y reportes

En seguridad aprendí que Django ya trae un sistema de autenticación muy completo y que la clave está en configurarlo bien: proteger cada vista, usar permisos por rol y entender por qué el cierre de sesión debe hacerse con POST y token CSRF. En reportes practiqué las consultas avanzadas del ORM, la diferencia entre `aggregate` y `annotate` y cómo agrupar por mes. Fue interesante ver cómo una misma consulta sirve para el reporte y para el dashboard. Como mejora, agregaría reportes en PDF y un registro de qué usuario creó o modificó cada reservación.

# 10. Referencias

- Django Software Foundation. (s. f.). *Django documentation, version 5.2*. https://docs.djangoproject.com/es/5.2/
- Django Software Foundation. (s. f.). *Writing your first Django app*. https://docs.djangoproject.com/es/5.2/intro/tutorial01/
- Bootstrap Team. (s. f.). *Bootstrap 5.3 documentation*. https://getbootstrap.com/docs/5.3/
- Chart.js Contributors. (s. f.). *Chart.js documentation*. https://www.chartjs.org/docs/latest/
- GitHub. (s. f.). *GitHub Docs: About pull requests*. https://docs.github.com/es/pull-requests
- Python Software Foundation. (s. f.). *Python 3 documentation*. https://docs.python.org/es/3/
