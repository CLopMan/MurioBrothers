import pyxel

class Bloque():
    def __init__(self, x, y, sprite):
        self.x: int = x
        self.y: int = y
        self.sprite: tuple = sprite

    def move(self, px):
        self.x -= px

    """def colision(self, other):
        """"""Función que comprueba colisiones entre entidades y bloques (aux[0] = esquina superior izquierda,
        aux[1] = esquina superior derecha, aux[2] = esquina inferior derecha, aux[3] = esquina inferior izquierda)
        Intento fallido
        """"""
        aux = [False, False, False, False]
        # Comprobación de que mario colisione con la esquina sup. izq.
        if abs(other.position[0] + other.size[0]/2 - self.x) < 8 and (
                abs(other.position[1] + other.size[1]/2 - self.y) < 8):
            aux[0] = True
        # Comprobación de que Mario colisione con la esquina sup. derecha
        if abs(other.position[0] + other.size[0] / 2 - (self.x + 16)) < 8 and (
                abs(other.position[1] + other.size[1] / 2 - self.y) < 8):
            aux[1] = True
        # Comprobación de que mario colisione con la esquina inferior derecha
        if abs(other.position[0] + other.size[0] / 2 - (self.x + 16)) < 8 and (
                abs(other.position[1] + other.size[1] / 2 - (self.y + 16)) < 8):
            aux[2] = True
        # Comprobación que mario colisione con la esquina inferior izquierda
        if abs(other.position[0] + other.size[0] / 2 - self.x) < 8 and (
                abs(other.position[1] + other.size[1] / 2 - (self.y + 16)) < 8):
            aux[3] = True
        aux = tuple(aux)
        return aux"""

    def colision2(self, other):
        """Función para comprobar la posición de mario o un enemigo con respecto de un bloque"""
        aux = [False, False, False, False, self.y, self.x]
        # Other está a la izquierda
        if self.x - other.position[0] >= 16:
            aux[0] = True
        # Other está en el rango en x del bloque
        elif abs(self.x - other.position[0]) < 16:
            aux[1] = True
        # Si other está a la derecha significa que los anteriores dos son falsos
        # Other está encima
        if self.y - other.position[1] >= 16:
            aux[2] = True
            aux[4] = self.y - other.size[1]
        # Other está debajo
        elif self.y - other.position[1] <= -16:
            aux[3] = True
        return aux

    def draw(self):
        """Funcion para el dibujo de bloques"""
        pyxel.blt(self.x, self.y, *self.sprite, colkey=2)