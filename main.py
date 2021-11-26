import pyxel
from tablero import Tablero
from mario import Mario
tablero = Tablero(0,0)


W = 256
H = 256
CAPTION = "MARIO BROSS"

def update():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
    tablero.inputs()
    tablero.update()


def draw():
    pyxel.cls(0)
    tablero.draw()



pyxel.init(W, H, caption=CAPTION)

pyxel.load("mario_assets.pyxres")

pyxel.run(update, draw)
