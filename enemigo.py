import pyxel
class Enemigo:
    def __init__(self, x, y, tipo, sprite):
        self.x = x
        self.y = y
        self.type = tipo
        self.sprite = sprite
    def draw(self):
        pyxel.blt(self.x, self.y, *self.sprite, colkey=10)
