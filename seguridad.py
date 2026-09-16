"""
seguridad.py
============
Toda la lógica de "quién ha iniciado sesión":

1. crear una SESIÓN cuando alguien hace login correctamente,
2. averiguar quién es el usuario mirando su COOKIE,
3. la DEPENDENCIA que protege las rutas privadas.

¿Cómo funciona una sesión en una web? (la idea clave)
-----------------------------------------------------
HTTP no tiene memoria: cada petición llega "suelta", el servidor
no sabe de quién es. La solución clásica:

- Cuando haces login, el servidor crea un TOKEN (un código secreto
  aleatorio) y se lo entrega en una COOKIE. La cookie viaja pegada
  a todas tus siguientes peticiones, como un carnet.
- El servidor apunta en su "libreta" qué token pertenece a cada
  usuario. Aquí la libreta es el diccionario `sesiones`, guardado
  en disco (`sesiones.json`) para que no se pierda al reiniciar.

No se usan ni OAuth2 ni JWT ni hashes: es la versión más simple
posible para ENTENDER el mecanismo. (En la vida real todo esto
se hace con más protecciones; mira la guía del profesor.)
"""

import json
import secrets  # para generar tokens aleatorios imposibles de adivinar
from pathlib import Path

from fastapi import Depends, HTTPException, Request
from typing import Annotated

from usuarios import Usuario, buscar_usuario, usuarios_db

# Nombre de la cookie donde guardamos el token de sesión.
COOKIE_SESION = "sesion"

# Cuánto vive la cookie en el navegador (en segundos): una semana.
# Sin esto, la cookie moriría al cerrar el navegador.
VIDA_SESION_SEGUNDOS = 7 * 24 * 60 * 60

# La "libreta" de sesiones abiertas: {token: username}.
# La guardamos en este archivo para que SOBREVIVA a los reinicios
# del servidor (junto a este código: no depende de la carpeta
# desde la que se arranque).
ARCHIVO_SESIONES = Path(__file__).parent / "sesiones.json"


def cargar_sesiones() -> dict[str, str]:
    """Lee la libreta del disco al arrancar. Si no existe aún, vacía."""
    if ARCHIVO_SESIONES.exists():
        return json.loads(ARCHIVO_SESIONES.read_text(encoding="utf-8"))
    return {}


def guardar_sesiones() -> None:
    """Escribe la libreta en el disco: así no se pierde al reiniciar."""
    ARCHIVO_SESIONES.write_text(json.dumps(sesiones), encoding="utf-8")


# Al arrancar, la libreta en memoria se llena leyendo el archivo.
sesiones: dict[str, str] = cargar_sesiones()


def crear_sesion(username: str) -> str:
    """Crea una sesión nueva y devuelve su token. (PASO 3 del diagrama)"""
    token = secrets.token_hex(16)  # 32 caracteres aleatorios, p. ej. "9f3c..."
    sesiones[token] = username     # apuntamos: "este token es de este usuario"
    guardar_sesiones()             # volcamos la libreta al disco
    return token


def cerrar_sesion(token: str) -> None:
    """Borra una sesión de la libreta (el usuario queda deslogueado)."""
    sesiones.pop(token, None)
    guardar_sesiones()             # el disco también se queda al día


def comprobar_login(username: str, password: str) -> Usuario | None:
    """
    Comprueba si el usuario existe y la contraseña coincide.
    (Es el PASO 2 del diagrama: diagrama-login.svg)

    Devuelve el Usuario si todo es correcto, o None si falla algo.
    Aquí la comprobación es una simple comparación de texto, porque
    (por decisión didáctica) NO usamos hashes en este proyecto.
    """
    datos = usuarios_db.get(username)
    if datos is None:
        return None                       # ese usuario no existe
    if datos["password"] != password:
        return None                       # la contraseña no coincide
    return buscar_usuario(username)       # ¡correcto! devolvemos el usuario


def get_current_user(request: Request) -> Usuario:
    """
    La DEPENDENCIA que protege las rutas privadas. El corazón del proyecto.
    (PASO 6: se ejecuta en CADA página privada antes de mostrarla.)

    En FastAPI, una dependencia es una función que se ejecuta ANTES de
    una ruta. Esta lee la cookie, busca la sesión y:

    - si hay sesión válida -> devuelve el Usuario y la ruta continúa;
    - si NO hay sesión     -> responde con una redirección al /login.

    Como las rutas piden al usuario así:  usuario: UsuarioDep
    ...cualquier ruta que declare ese parámetro queda protegida sola.
    """
    token = request.cookies.get(COOKIE_SESION)      # lee la cookie (o None)
    username = sesiones.get(token or "")            # busca en la libreta
    if username is None:
        # No hay sesión: redirigimos al login con el código 303
        # ("ve a otra página"). El navegador lo sigue automáticamente.
        raise HTTPException(
            status_code=303,
            headers={"Location": "/login"},
        )
    return buscar_usuario(username)


# Apodo cómodo para pedir "el usuario conectado" en cualquier ruta.
# Es un ALIAS de tipo: en las rutas escribimos solo `usuario: UsuarioDep`.
UsuarioDep = Annotated[Usuario, Depends(get_current_user)]