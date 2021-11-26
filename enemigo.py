import pyxel

import constantes


class Enemigo:
    def __init__(self, x, y, tipo, sprite):
        self.x = x
        self.y = y
        self.velocidad = [0, 0]
        self.type = tipo
        self.sprite = sprite
        # dirección
        self.dir = -1

    def cuerpoTierra(self):
        """gravedad"""
        # temporalmente el suelo está en 208, si se pasa hacia abajo corrige el error
        if self.y > 208:
            # velocidad vertical = 0
            self.velocidad[1] = 0
            # corrige la posición
            self.y = 208

        elif self.y < 206:
            self.velocidad[1] += constantes.GRAVEDAD
            self.y += self.velocidad[1]
        else:
            self.y = 208



    def draw(self):
        pyxel.blt(self.x, self.y, *self.sprite, colkey=10)

    def move(self):
        self.x += self.dir * constantes.VELOCIDAD_ENEMIGOS
    def cambioDir(self):
        self.dir *= -1
