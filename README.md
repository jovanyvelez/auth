# Login simple con FastAPI + Jinja2

Una mini-aplicación web didáctica: **un formulario de login con sesiones
de cookie**, una home con menú y dos páginas privadas. Está construida
con FastAPI y plantillas Jinja2, y es la versión *más simple posible*
del ejemplo de autenticación de la documentación oficial de FastAPI.

> ⚠️ Es un proyecto **para aprender**. Deliberadamente no usa OAuth2,
> ni JWT, ni hashes de contraseña (mira la guía del profesor para
> saber qué cambiaría en la vida real).

## Cómo arrancarlo

```bash
uv sync        # instala las dependencias la primera vez
fastapi dev    # arranca el servidor de desarrollo
```

Abre <http://127.0.0.1:8000> en el navegador: cualquier página te
llevará al login.

**Usuarios de prueba:**

| Usuario | Contraseña |
|---------|------------|
| `ana`   | `1234`     |
| `luis`  | `abcd`     |

## Estructura del proyecto

```
main.py            → punto de entrada: crea la app y añade las rutas
rutas.py           → las páginas web (login, home, perfil, objetos, logout)
seguridad.py       → sesiones con cookie + la dependencia que protege rutas
usuarios.py        → los datos: usuarios (¡contraseñas en claro!) y objetos
diagrama-login.svg → el recorrido del login en dibujo (PASO 1 a 7)
sesiones.json      → la "libreta" de sesiones en disco (se crea sola)
templates/         → las plantillas HTML (Jinja2)
  base.html        → estructura común + menú
  login.html       → formulario de login
  home.html        → bienvenida
  perfil.html      → página 1 del menú
  objetos.html     → página 2 del menú
GUIA_ESTUDIANTE.md → guía para seguir el proyecto paso a paso
GUIA_PROFESOR.md   → guía didáctica para el aula
```

## Despliegue en Vercel (opcional)

La web puede verse en internet con configuración casi cero: `main.py`
con la `app` es un punto de entrada que Vercel reconoce solo.

1. En [vercel.com](https://vercel.com) → *Add New → Project* → importa
   el repo de GitHub.
2. Vercel detecta FastAPI, instala `requirements.txt` y usa el Python de
   `.python-version` (3.14). No hay nada más que configurar.

Roles de los archivos: `requirements.txt` = dependencias para la nube;
`vercel.json` = excluye del despliegue `.venv` y datos locales.

> ⚠️ En Vercel el disco es de solo lectura: las sesiones viven solo en
> la memoria de la función. Si la función «se enfría» (*cold start*),
> hay que repetir el login. En local sí se guardan en `sesiones.json`.

## Documentación

- **Diagrama:** `diagrama-login.svg` — el flujo del login en 7 pasos (los
  mismos «PASO n» de los comentarios del código).
- **Alumno:** lee `GUIA_ESTUDIANTE.md` (funcionamiento, tour por el
  código y ejercicios).
- **Profesor:** `GUIA_PROFESOR.md` (objetivos, plan de clase,
  soluciones y advertencias de seguridad).