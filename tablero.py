import pyxel
import constantes
from interfaz import Interfaz
from mario import Mario


class Tablero:
    def __init__(self, velocidad, x):
        self.velocidad: float
        self.x: float
        self.interfaz = Interfaz(0, 999, 0, 1, 1, 3)
        self.enemigos = []
        self.bloques = []
        self.mario = Mario(*constantes.posicion_inicial_mario)

    def inputs(self):
        """Recoge los distintos usuarios del jugador"""
        self.mario.set_velocidad()
        if pyxel.btn(pyxel.KEY_LEFT):
            self.mario.moverIzquierda()
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.mario.moverDerecha()
        if pyxel.btn(pyxel.KEY_Z):
            self.mario.salto()

    def update(self):
        self.mario.update()



    def draw(self):
        pyxel.bltm(0,0, 0, 0, 32, 256, 256)
        self.interfaz.draw()
        self.mario.draw()
