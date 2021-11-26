import pyxel
import constantes
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
        self.sprite: list = [0, 16, 0, 16, 16]
        # disparador de salto
        self.__saltar = False
        # contador de frames en el aire
        self.__frames_aire = 0
        # comprobación de que mario está en el suelo
        self.__en_suelo = True

    @property
    def aceleracion(self):
        if self.correr:
            return 0.6
        else:
            return 0.25



    # MOVIMIENTO HORIZONTAL

    def set_velocidad(self):
        if self.velocidad[0] < 3:
            self.velocidad[0] += self.aceleracion
        elif self.velocidad[0] > 3:
            self.velocidad[0] = 3

    def moverDerecha(self):
        self.position[0] += self.velocidad[0]

    def moverIzquierda(self):
        self.position[0] -= self.velocidad[0]

    # MOVIMIENTO VERTICAL

    def gravedad(self):
        """establece una aceleración hacia abajo del personaje siempre que este se despegue del suelo"""
        if not self.__en_suelo:
            self.velocidad[1] += constantes.GRAVEDAD
            self.__frames_aire += 1

    def cuerpoTierra(self):
        """esta función controla que el jugador esté pisando el suelo, si no lo está pisando cuenta los frames que está
        en el aire"""
        # temporalmente el suelo está en 208, si se pasa hacia abajo corrige el error
        if self.position[1] > 208:
            self.__en_suelo = True
            # resetea el valor de frames en el aire
            self.__frames_aire = 0
            # velocidad vertical = 0
            self.velocidad[1] = 0
            # corrige la posición
            self.position[1] = 208
        elif self.position[1] < 208:
            self.__en_suelo = False

    def salto(self):
        """Establece una aceleración vertical durante un máximo de 7 frames en los que se mantenga pulsada la tecla
        correspondiente. Con esto permitimos que haya 7 alturas de salto dependiendo de cuánto se pulso el botón"""
        if self.__en_suelo or self.__frames_aire < 7:
            self.velocidad[1] -= 1.5

    def update(self):
        self.position[1] += self.velocidad[1]
        self.cuerpoTierra()
        self.gravedad()

    def draw(self):
        pyxel.blt(self.position[0], self.position[1], *self.sprite, colkey=0)
        pyxel.text(0, 15, "%s\n%s, %s\n%i\n%s\n%s" % (
            self.position, self.velocidad[0], self.velocidad[1], self.__frames_aire, self.__en_suelo, self.sprite), 0)