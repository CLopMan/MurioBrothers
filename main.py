"""Módulo principal: tamaño de ventaja e inicialización del juego"""

import pyxel
from tablero import Tablero
import constantes

# Objeto tablero: recoge todas las interacciones entre objetos y la cámara
tablero = Tablero(constantes.WIDTH, constantes.HEIGHT, constantes.VELOCIDAD, constantes.X, 0)


def update():
    """Actualiza constantemente el programa"""
    # Para salir del programa
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
    # Inputs
    tablero.inputs()
    tablero.update()


def draw():
    # Fondo
    pyxel.cls(0)
    tablero.draw()


# Título de la ventana
CAPTION = "MARIO BROS"

# Inicialización de ventana
pyxel.init(tablero.w, tablero.h, caption=CAPTION, fullscreen=True)

# Carga de imágenes
pyxel.load("mario_assets.pyxres")

# Ejecución del juego
pyxel.run(update, draw)
