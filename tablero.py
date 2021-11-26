import pyxel

class Tablero:
    def __init__(self, velocidad, x):
        self.velocidad: float
        self.x: float

    def inputs(self, player):
        player.velocidad()
        if pyxel.btn(pyxel.KEY_LEFT):
            player.moveIzquierda()
        if pyxel.btn(pyxel.KEY_RIGHT):
            player.moveDerecha()

    def draw(self):
        pyxel.bltm(0,0, 0, 0, 0, 256, 256)
