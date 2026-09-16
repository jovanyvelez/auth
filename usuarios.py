"""
usuarios.py
===========
Aquí viven los DATOS de la aplicación: los usuarios y sus objetos.

En un proyecto real estos datos estarían en una base de datos
(SQLite, PostgreSQL...). Para aprender usamos simples diccionarios
de Python: son fáciles de leer y de modificar.

Separar los datos en su propio archivo es lo que se llama
"separación de responsabilidades": cada archivo hace UNA cosa.
"""

from pydantic import BaseModel


class Usuario(BaseModel):
    """
    El "carnet de identidad" de un usuario de la web.

    Pydantic (BaseModel) convierte un diccionario normal en un objeto
    con campos comprobados. Fíjate que aquí NO está la contraseña:
    esos datos son los "públicos", los que la web puede mostrar.
    """

    username: str           # nombre de usuario (único), p. ej. "ana"
    nombre_completo: str    # p. ej. "Ana García"
    email: str              # p. ej. "ana@example.com"


# ---------------------------------------------------------------------------
# "Base de datos" de usuarios: la clave de cada entrada es el username.
#
# ¡ATENCIÓN! La contraseña se guarda en TEXTO PLANO a propósito:
# este proyecto solo quiere enseñar CÓMO funciona un login.
# En un proyecto real NUNCA se guarda la contraseña tal cual:
# se guarda un hash (una huella irreversible) de la contraseña.
# ---------------------------------------------------------------------------
usuarios_db: dict[str, dict] = {
    "ana": {
        "username": "ana",
        "nombre_completo": "Ana García",
        "email": "ana@example.com",
        "password": "1234",
    },
    "luis": {
        "username": "luis",
        "nombre_completo": "Luis Pérez",
        "email": "luis@example.com",
        "password": "abcd",
    },
}


# Los "objetos" (items) de cada usuario, para tener una segunda página
# que muestre datos privados. Cada lista pertenece a un usuario.
items_db: dict[str, list[str]] = {
    "ana": ["Bicicleta", "Libro de Python", "Auriculares"],
    "luis": ["Guitarra", "Cámara de fotos"],
}


def buscar_usuario(username: str) -> Usuario | None:
    """
    Busca un usuario por su username.

    Devuelve el objeto Usuario si existe, o None si no existe.
    Convertir diccionario -> objeto Usuario se hace desempaquetando:
    Usuario(**datos) es lo mismo que escribir cada campo uno a uno.
    """
    datos = usuarios_db.get(username)
    if datos is None:
        return None
    return Usuario(**datos)