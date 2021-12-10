import pyxel
import constantes


class Bloque():
    """En esta clase están las funciones de los bloques"""
    def __init__(self, x, y, sprite):
        self.x: int = x
        self.y: int = y
        self.sprite: tuple = sprite

    def move(self, px):
        """Mueve los bloques con la velocidad de la cámara"""
        self.x -= px

    def colision2(self, other):
        """Función para comprobar la posición de mario o un enemigo con respecto de un bloque"""
        aux = [False, False, False, False, self.y, self.x]
        # Other está a la izquierda
        if self.x - other.position[0] >= other.size[0]:
            aux[0] = True
        # Other está en el rango en x del bloque
        elif abs(self.x - other.position[0]) < other.size[0]:
            aux[1] = True
        # Si other está a la derecha significa que los anteriores dos son falsos
        # Other está encima
        if self.y - other.position[1] >= other.size[1]:
            aux[2] = True
            aux[4] = self.y - other.size[1]
        # Other está debajo
        elif self.y - other.position[1] <= -16:
            aux[3] = True
        return aux

    def cambioBloqueLiso(self):
        self.sprite = constantes.SPRITE_LISO

    def draw(self):
        """Funcion para el dibujo de bloques"""
        pyxel.blt(self.x, self.y, *self.sprite, colkey=2)