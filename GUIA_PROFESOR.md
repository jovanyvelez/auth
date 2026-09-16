# Guía del profesor — Login simple con FastAPI + Jinja2

Proyecto didáctico derivado del ejemplo de autenticación de la
documentación oficial de FastAPI, **simplificado a propósito** para un
primer contacto con el desarrollo web. Esta guía explica qué se cambió
y por qué, propone un plan de clase y da soluciones de los ejercicios.

---

## 1. Objetivos didácticos

Al terminar, el estudiante debe ser capaz de:

1. Explicar **por qué una web necesita login/sesiones** (HTTP no tiene
   memoria entre peticiones).
2. Seguir el flujo completo: formulario → POST → creación de sesión →
   cookie → peticiones siguientes → logout.
3. Leer un proyecto con **separación de responsabilidades** (datos /
   seguridad / rutas / plantillas / ensamblado) y localizar en qué
   archivo vive cada cosa.
4. Reconocer los mecanismos de FastAPI usados: rutas GET/POST,
   **dependencias** (`Depends`) como punto único de protección,
   `Form` para datos de formulario, `RedirectResponse` y Jinja2.
5. Modificar y ampliar la aplicación con ejercicios guiados.

No se persigue: OAuth2, JWT, hashes, bases de datos, seguridad real.
Son el "siguiente paso", no la primera lección.

## 2. Qué se eliminó del ejemplo oficial y por qué

| Elemento del ejemplo de la documentación | Decisión aquí | Motivo didáctico |
|---|---|---|
| `OAuth2PasswordBearer` + token Bearer | Sesión con **cookie** | El navegador gestiona la cookie solo; el alumno ve el mecanismo completo sin entender cabeceras `Authorization` |
| JWT (`pyjwt`) con `SECRET_KEY` y expiración | Token aleatorio en un JSON (`secrets.token_hex`) | "La libreta de sesiones" es una metáfora directa; JWT exige cifrado/clave/expiración para explicarse bien |
| Hash de contraseñas (`pwdlib`) | Comparación en texto plano | Se aísla la lección en "cómo funciona el login"; el hashing es otra lección |
| Modelo `disabled` / usuarios inactivos | Eliminado | Aporta ramas de código sin valor didáctico a este nivel |
| `Token`/`TokenData` (Pydantic) | Solo `Usuario` | Menos piezas que siguen el hilo |
| JSON como respuesta | **HTML con Jinja2** | El objetivo es una web navegable, no una API |

**Importante — mensaje para la clase:** el resultado *no es* código de
producción. Hacerlo explícito convierte la omisión en contenido:

- Texto plano en contraseñas: en producción, **hash** (p. ej. Argon2
  o bcrypt) — nunca reversible.
- `sesiones` en un JSON simple: en producción, un almacén pensado
  para ello (BD, Redis), cookies firmadas y caducidad real.
- Sin HTTPS: en producción, las cookies viajan con `Secure`,
  `HttpOnly` y `SameSite`.

## 3. Estructura y dónde se enseña cada concepto

```
main.py     → ensamblado de la aplicación (app.include_router)
rutas.py    → rutas GET/POST, Form, RedirectResponse, TemplateResponse
seguridad.py→ dependencias (Depends), cookies, sesiones, persistencia JSON
usuarios.py → modelo Pydantic, diccionarios como "base de datos"
templates/  → herencia de plantillas, filtros, {% if %} / {% for %}
```

La protección de rutas recae en **una única función**
(`get_current_user`, alias `UsuarioDep`): cualquier ruta que declare
`usuario: UsuarioDep` queda protegida. Es el concepto nuclear del
proyecto; dedícale tiempo.

Coherencia didáctica: el diagrama (`diagrama-login.svg`), la guía del
estudiante y los comentarios del código usan los mismos números
**PASO 1-7**. Esa triple codificación (imagen ↔ texto ↔ código) es la
que permite al alumnado orientarse sin ayuda.

Rutas públicas deliberadas: `/login` (GET y POST) y `/logout`.
Pregunta que abre la clase: *"¿Qué pasaría si el login exigiera
haber iniciado sesión?"*

## 4. Plan de sesión sugerido (90 min)

1. **Demo inicial (10 min)** — arrancar la app; intentar `/perfil`
   sin sesión; login correcto e incorrecto; logout. Ver la cookie en
   las herramientas de desarrollador.
2. **La idea de la sesión (15 min)** — proyectar `diagrama-login.svg`
   (el recorrido PASO 1-7; también puede imprimirse como póster) y
   dibujar en pizarra el diagrama navegador/servidor de la guía del
   estudiante (sección 2).
   Insistir: *el carnet (cookie) va y viene; la libreta vive en el
   servidor*.
3. **Tour del código (25 min)** — seguir el orden
   `usuarios → seguridad → rutas → templates → main`, con el código
   proyectado. Preguntar en cada archivo "¿quién llama a esto?".
4. **Práctica guiada (25 min)** — ejercicios 1-3 de la guía del
   estudiante, en parejas.
5. **Cierre (15 min)** — puesta en común; discusión de "¿dónde está
   el fallo de seguridad?" (contraseñas en claro, sesiones en
   memoria); anunciar los conceptos "de la vida real".

## 5. Errores típicos del alumnado (y cómo diagnosticarlos)

| Síntoma | Causa probable | Dónde mirar |
|---|---|---|
| `jinja2.exceptions.TemplateNotFound` | plantilla mal escrita o fuera de `templates/` | nombre en `TemplateResponse` |
| La página no muestra el usuario | falta `context={"usuario": usuario}` | `rutas.py` |
| El menú no aparece | la ruta no pasa `usuario` (no protegida) | `rutas.py` + `base.html` (`{% if usuario %}`) |
| Tras el login no hay sesión | falta `respuesta.set_cookie(...)` | `enviar_login` |
| No entra tras el login (bucle) | token no se guardó en `sesiones` o la cookie no viaja | `seguridad.crear_sesion` / cookie en DevTools |
| `422 Unprocessable Entity` al enviar el form | los `name` del HTML no coinciden con los parámetros de `Form()` | `login.html` vs `rutas.py` |
| Cambios que no aparecen | plantilla cacheada o servidor parado | reiniciar `fastapi dev` |
| "Tengo la cookie pero me manda al login" | se borró/editó mal `sesiones.json` | contenido del archivo y reinicio |

## 6. Soluciones de los ejercicios (guía del estudiante)

**1. Email en la home.** En `home.html`:
`<p>{{ usuario.email }}</p>` (no requiere Python).

**2. Contar objetos en la home.** Pasar la lista desde la ruta y usar
el filtro `length`:

```python
# rutas.py — home()
objetos_del_usuario = items_db.get(usuario.username, [])
... context={"usuario": usuario, "objetos": objetos_del_usuario}
```
```html
{# home.html #}
<p>Tienes {{ objetos|length }} objetos.</p>
```

**3. Página /saludos.**

```python
# rutas.py
@router.get("/saludos")
def saludos(request: Request, usuario: UsuarioDep):
    return templates.TemplateResponse(
        request=request, name="saludos.html", context={"usuario": usuario})
```
```html
{# templates/saludos.html #}
{% extends "base.html" %}
{% block contenido %}<h1>¡Buenos días, {{ usuario.nombre_completo }}!</h1>{% endblock %}
```
Y en `base.html`: `<a href="/saludos">Saludos</a>`. Comprobación de
que entendieron la protección: sin sesión, `/saludos` debe redirigir
al login **solo por declarar `usuario: UsuarioDep`**.

**4. Contador de visitas.** Un diccionario `visitas: dict[str, int]`
en `rutas.py`; en `home()` incrementar
`visitas[usuario.username] = visitas.get(usuario.username, 0) + 1`
y pasar el valor al contexto. Discutible: la memoria del servidor
también se borra al reiniciar → puente hacia bases de datos.

**5. Página de error.** Crear `templates/error.html` (extiende base)
y en `enviar_login` devolver
`templates.TemplateResponse(request=request, name="error.html", context={"error": "..."})`.

**6. (Reto) Explora la libreta.** Editando `sesiones.json` con el
servidor parado (cambiar el `username` que acompaña al propio
token), al arrancar la web muestra los datos del otro usuario:
*quien tiene tu token, es tú*. Puente ideal para discutir el
secuestro de sesión, por qué los tokens se generan con
`secrets.token_hex` (imposibles de adivinar) y qué aportan en
producción las cookies firmadas y la caducidad real. Variante
rápida: borrar el archivo y comprobar que hay que repetir login.

## 7. Evaluación sugerida (rúbrica mínima)

| Criterio | Insuficiente | Suficiente | Sobresaliente |
|---|---|---|---|
| Protección | alguna ruta pública expone datos | todas las privadas piden `UsuarioDep` | añade rutas nuevas ya protegidas |
| Sesión | no sabe explicar la cookie | explica cookie + libreta | explica qué falla de esta sesión en producción |
| Plantillas | copia HTML sin herencia | usa `{% extends %}` y `{{ }}` | usa `{% if %}`/`{% for %}` con datos nuevos |
| Estilo | código sin comentar | comenta lo que cambia | refactoriza manteniendo la separación de responsabilidades |

## 8. Para ampliar en próximas sesiones

1. Hash de contraseñas (regreso al ejemplo oficial de la documentación).
2. Base de datos real (SQLite + SQLModel) en lugar de diccionarios.
3. Registro de usuarios nuevos (form de alta) y validación de datos.
4. Cookies firmadas (`itsdangerous`) o JWT, y comparar las dos.
5. Despliegue: qué cambia (`fastapi run`, HTTPS, variables de entorno).