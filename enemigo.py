import pyxel

import constantes

from entidad import Entidad

class Enemigo():
    def __init__(self, x, y, suelo, sprite):
        self.position = [x, y]
        self.suelo = suelo
        self.sprite = sprite
        self.velocidad = [0, 0]
        # dirección
        self.direccion = -1

    def cuerpoTierra(self):
        """gravedad"""
        # temporalmente el suelo está en 208, si se pasa hacia abajo corrige el error
        if self.position[1] > 208:
            # velocidad vertical = 0
            self.velocidad[1] = 0
            # corrige la posición
            self.position[1] = 208

        elif self.position[1] < 206:
            self.velocidad[1] += constantes.GRAVEDAD
            self.position[1] += self.velocidad[1]
        else:
            self.position[1] = 208

    def cambioDir(self):
        self.direccion *= -1

    def draw(self):
        pyxel.blt(self.position[0], self.position[1], *self.sprite, colkey=10)

    def update(self):
        self.move()
        self.cuerpoTierra()

    def move(self):
        self.position[0] += self.direccion * constantes.VELOCIDAD_ENEMIGOS
