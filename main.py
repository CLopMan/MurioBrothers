import pyxel

W = 256
H = 256
CAPTION = "MARIO BROSS"

def update():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    pyxel.cls(0)


pyxel.init(W, H, caption=CAPTION)

pyxel.load("mario_assets.pyxres")

pyxel.run(update, draw)
