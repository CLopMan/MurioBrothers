import pyxel
from tablero import Tablero
import constantes

# Objeto tablero: recoge todas las interacciones entre objetos y la cámara
tablero = Tablero(constantes.WIDTH, constantes.HEIGHT, constantes.VELOCIDAD, constantes.X)


def update():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
    tablero.inputs()
    tablero.update()


def draw():
    pyxel.cls(0)
    tablero.draw()


# Título de la ventana
CAPTION = "MARIO BROSS"

# inicialización de ventana
pyxel.init(tablero.w, tablero.h, caption=CAPTION)

# Carga de imágenes
pyxel.load("mario_assets.pyxres")

# ejecución del juego
pyxel.run(update, draw)
