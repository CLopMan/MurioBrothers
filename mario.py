import pyxel


class Mario:
    """personaje principal, conjunto de todos los parámetros necesiarios"""

    def __init__(self, x, y):
        # posición x e y
        self.position: list = [x, y]
        # velocidad en x e y
        self.velocidad: list = [0.0, 0.0]
        # direccion (1 = derecha, -1 = izquierda)
        self.direccion = 0
        # sprintar
        self.correr = False
        # control de sprite
        self.sprite: list = [0, 0, 0, 16, 16]

    def velocidad(self):
        self.velocidad[0] = 2.5

    def moveDerecha(self):
        self.position[0] += self.velocidad[0]

    def moveizquierda(self):
        self.position -= self.velocidad[0]

    def parriba(self):
        self.velocidad[1] += 2.5

    def salto(self):
        self.position[1] -= self.velocidad[1]