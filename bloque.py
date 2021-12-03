import pyxel

class Bloque():
    def __init__(self, x, y, sprite):
        self.x: int = x
        self.y: int = y
        self.sprite: tuple = sprite

    def move(self, px):
        self.x -= px

    def draw(self):
        pyxel.blt(self.x, self.y, *self.sprite)

    def colision(self, other):
        """Función que comprueba colisiones entre entidades y bloques (aux[0] = esquina superior izquierda,
        aux[1] = esquina superior derecha, aux[2] = esquina inferior derecha, aux[3] = esquina inferior izquierda)"""
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
        print(aux)
        return aux