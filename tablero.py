import pyxel
from interfaz import Interfaz
from mario import Mario
class Tablero:
    def __init__(self, velocidad, x):
        self.velocidad: float
        self.x: float
        self.interfaz = Interfaz(0, 999, 0, 1, 1, 3)
        self.enemigos = []
        self.bloques = []

    def inputs(self, player):
        player.set_velocidad()
        if pyxel.btn(pyxel.KEY_LEFT):
            player.moverIzquierda()
        if pyxel.btn(pyxel.KEY_RIGHT):
            player.moverDerecha()

    def draw(self):
        pyxel.bltm(0,0, 0, 0, 32, 256, 256)
        self.interfaz.draw()
