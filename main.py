import pyxel
from tablero import Tablero
import constantes

tablero = Tablero(constantes.WIDTH, constantes.HEIGHT, constantes.VELOCIDAD, constantes.X)

CAPTION = "MARIO BROSS"


def update():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
    tablero.inputs()
    tablero.update()


def draw():
    pyxel.cls(0)
    tablero.draw()


pyxel.init(tablero.w, tablero.h, caption=CAPTION)

pyxel.load("mario_assets.pyxres")

pyxel.run(update, draw)
