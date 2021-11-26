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
        self.sprite: list = [0, 16,0, 16, 16]
    @property
    def aceleracion(self):
        if self.correr:
            return 0.6
        else:
            return 0.25

    def set_velocidad(self):
        if self.velocidad[0] < 3:
            self.velocidad[0] += self.aceleracion
        elif self.velocidad[0] > 3:
            self.velocidad[0] = 3

    def moverDerecha(self):
        self.position[0] += self.velocidad[0]

    def moverIzquierda(self):
        self.position[0] -= self.velocidad[0]

    def parriba(self):
        self.velocidad[1] += 2.5

    def salto(self):
        self.position[1] -= self.velocidad[1]
    def draw(self):
        pyxel.blt(self.position[0], self.position[1], *self.sprite)