import pyxel
import constantes

class Entidad:
    def __init__(self, x, y, suelo, sprite):
        self.position: list = [x, y]
        self.size: list = [16, 16]
        self.sprite: list = sprite
        self.velocidad = [0, 0]
        self.suelo = suelo


    @property
    def acel_gravedad(self):
        return constantes.GRAVEDAD

    def gravedad(self):
        """Aplica una aceleración hacia abajo si mario se despega del __suelo"""
        if not self.__en_suelo:
            self.velocidad[1] += self.acel_gravedad

