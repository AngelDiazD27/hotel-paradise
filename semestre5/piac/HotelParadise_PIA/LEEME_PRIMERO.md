# PIA Hotel Paradise — Léeme primero

Todo lo necesario para entregar el PIA de Django entre los 5 integrantes.

| Carpeta / archivo | Para qué es |
|---|---|
| `GUIA_EQUIPO.docx` (y `.md`) | **Empiecen aquí.** Roles, cómo crear el repo en GitHub, qué hace cada integrante fase por fase, comandos, errores comunes, guion del video y preguntas de repaso. |
| `paquetes_por_fase/` | Los archivos que cada integrante copia a su repo en su turno (Fases 1 a 8). |
| `proyecto_completo/` | El sistema terminado, para correrlo ya y comparar. |
| `entregables/` | Documento Técnico y Manual de Usuario en Word, más los diagramas. |

## Probar el sistema en 2 minutos

```bash
cd proyecto_completo
python -m venv venv
venv\Scripts\activate          # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py cargar_demo
python manage.py runserver
```

Abre http://127.0.0.1:8000 y entra con `admin` / `Paradise2026!` (o `recepcion` / `Recepcion2026!`).

## Antes de entregar

- Pongan sus nombres y matrículas en la portada del Documento Técnico y del Manual, y en el `README.md` (tabla "Equipo").
- Inserten los logotipos de la UANL y de FACPYA en las portadas.
- Cada integrante reescribe su conclusión individual (sección 9 del Documento Técnico y `docs/conclusiones/`).
- Al abrir los Word, si el índice sale vacío: clic derecho → Actualizar campos.
- Cambien `[usuario]` por el usuario real de GitHub en el Documento Técnico y en la última diapositiva.
