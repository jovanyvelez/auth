"""
main.py
=======
El PUNTO DE ENTRADA de la aplicación: aquí se "monta" la app.

Este archivo apenas contiene código, y eso es buena señal:
su única responsabilidad es juntar las piezas.

Arranca el servidor de desarrollo con:

    fastapi dev

y abre http://127.0.0.1:8000 en el navegador.

¿Te pierdes entre archivos? Abre diagrama-login.svg (el recorrido del
login en dibujo) y GUIA_ESTUDIANTE.md. Los comentarios del código
usan los mismos números: PASO 1 a PASO 7.
"""

from fastapi import FastAPI

# Las rutas (páginas) están en su propio archivo, rutas.py.
from rutas import router

# Creamos la aplicación FastAPI con un título (se ve en /docs).
app = FastAPI(title="Login simple con FastAPI + Jinja2")

# Añadimos TODAS las rutas definidas en rutas.py a la aplicación.
app.include_router(router)