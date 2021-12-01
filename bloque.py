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


