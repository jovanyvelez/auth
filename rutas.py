"""
rutas.py
========
Las RUTAS de la web: cada función es una página.

Convención HTTP que usamos:
- GET  -> "muéstrame una página".
- POST -> "tomo datos de un formulario".

Zonas de la web:
- PÚBLICA:  /login (GET y POST) y /logout. Tiene que ser pública:
  si el login exigiera haber iniciado sesión, ¡nadie podría entrar nunca!
- PRIVADA:  / , /perfil y /objetos. Todas piden `usuario: UsuarioDep`,
  y esa dependencia (seguridad.py) redirige al login si no hay sesión.
"""

from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from seguridad import (
    COOKIE_SESION,
    UsuarioDep,
    VIDA_SESION_SEGUNDOS,
    cerrar_sesion,
    comprobar_login,
    crear_sesion,
)
from usuarios import items_db

# Jinja2 busca las plantillas HTML dentro de la carpeta "templates".
# Ruta ABSOLUTA (relativa a este archivo): funciona igual en local y en
# la nube (Vercel), aunque la app no arranque desde la carpeta raíz.
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

# Un router es un "paquete de rutas" que main.py incluirá en la app.
router = APIRouter()


# ---------------------------------------------------------------------------
# LOGIN / LOGOUT (la zona pública)
# ---------------------------------------------------------------------------


@router.get("/login")
def formulario_login(request: Request):
    """Muestra el formulario de login (login.html)."""
    # TemplateResponse("pinta" una plantilla). Siempre necesita:
    # - request: la petición que está en curso,
    # - name: el archivo de plantilla,
    # - context: variables que la plantilla podrá usar.
    return templates.TemplateResponse(request=request, name="login.html")


@router.post("/login")
def enviar_login(
    request: Request,
    username: Annotated[str, Form()],  # campo "username" del formulario
    password: Annotated[str, Form()],  # campo "password" del formulario
):
    """
    Recibe el formulario, comprueba las credenciales y crea la sesión.
    (Son los PASO 2, 3 y 4 del diagrama: diagrama-login.svg)

    Dos caminos posibles:
    - mal:     volvemos a pintar el formulario con un mensaje de error;
    - correcto: creamos la sesión y redirigimos a la home (código 303,
      para que el navegador cambie de POST a GET).
    """
    usuario = comprobar_login(username, password)  # PASO 2: ¿existen y coinciden?
    if usuario is None:
        # Login incorrecto: misma página + mensaje de error para el usuario.
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Usuario o contraseña incorrectos."},
        )

    # Login correcto — PASO 3: creamos la sesión (token apuntado en la libreta)...
    token = crear_sesion(usuario.username)
    # ...PASO 4: redirigimos a la home y entregamos la cookie con el token.
    respuesta = RedirectResponse("/", status_code=303)
    # max_age le da "fecha de caducidad" a la cookie: vive una semana,
    # aunque el usuario cierre el navegador (antes moría al cerrarlo).
    respuesta.set_cookie(COOKIE_SESION, token, max_age=VIDA_SESION_SEGUNDOS)
    return respuesta


@router.get("/logout")
def logout(request: Request):
    """
    Cierra la sesión: borra el token de la libreta y la cookie del navegador.
    (Es el PASO 7 del diagrama: diagrama-login.svg)

    No muestra ninguna página: siempre acaba redirigiendo al login.
    """
    token = request.cookies.get(COOKIE_SESION)
    if token:
        cerrar_sesion(token)
    respuesta = RedirectResponse("/login", status_code=303)
    respuesta.delete_cookie(COOKIE_SESION)  # borra también el "carnet"
    return respuesta


# ---------------------------------------------------------------------------
# PÁGINAS PRIVADAS: cualquier persona sin sesión es enviada al /login
# automáticamente por la dependencia UsuarioDep (PASO 6 del diagrama).
# ¡Eso es "proteger una ruta"!
# ---------------------------------------------------------------------------


@router.get("/")
def home(request: Request, usuario: UsuarioDep):
    """Home: página de bienvenida con el menú hacia el resto de páginas."""
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"usuario": usuario},
    )


@router.get("/perfil")
def perfil(request: Request, usuario: UsuarioDep):
    """Página 1: los datos personales del usuario conectado."""
    return templates.TemplateResponse(
        request=request,
        name="perfil.html",
        context={"usuario": usuario},
    )


@router.get("/objetos")
def objetos(request: Request, usuario: UsuarioDep):
    """
    Página 2: los objetos del usuario conectado.

    Buscamos SU lista en items_db usando su username. Es una demo de
    datos privados: cada usuario solo ve los suyos.
    """
    objetos_del_usuario = items_db.get(usuario.username, [])
    return templates.TemplateResponse(
        request=request,
        name="objetos.html",
        context={"usuario": usuario, "objetos": objetos_del_usuario},
    )