import pyxel

import constantes


class Enemigo:
    def __init__(self, x, y, tipo, sprite):
        self.position = [x, y]
        self.velocidad = [0, 0]
        self.type = tipo
        self.sprite = sprite
        # dirección
        self.dir = -1

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

    def draw(self):
        pyxel.blt(self.position[0], self.position[1], *self.sprite, colkey=10)

    def move(self):
        self.position[0] += self.dir * constantes.VELOCIDAD_ENEMIGOS

    def cambioDir(self):
        self.dir *= -1
