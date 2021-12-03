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
        """Aplica una aceleración hacia abajo si mario se despega del suelo"""
        if not self.__en_suelo:
            self.velocidad[1] += self.acel_gravedad

    """def cuerpoTierra(self):
        esta función controla que el jugador esté pisando el suelo, si no lo está pisando cuenta los frames que está
        en el aire
        # temporalmente el suelo está en 208, si se pasa hacia abajo corrige el error
        if self.position[1] > 208:
            self.__en_suelo = True
            # velocidad vertical = 0
            self.velocidad[1] = 0
            # corrige la posición
            self.position[1] = 208
        elif self.position[1] < 208:
            self.__en_suelo = False"""