import pyxel
import constantes
from interfaz import Interfaz
from mario import Mario
from enemigo import Enemigo


class Tablero:
    def __init__(self, w, h, velocidad, x):
        self.w: int = w
        self.h: int = h
        # posición en x de la cámara
        self.x: float = x
        self.velocidad: float = velocidad
        self.interfaz: Interfaz = Interfaz(0, 999, 0, 1, 1, 3)
        # Lista de enemigos, de momento sólo he metido y colocado el primero
        self.enemigos: list = [Enemigo(*constantes.ENEMIGOS[0])]
        self.bloques: list = []
        self.mario: Mario = Mario(*constantes.posicion_inicial_mario)

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
        self.enemigos[0].draw()
