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

        # MOVIMIENTO
        # constantes
    @property
    def aceleracion(self):
        if self.correr:
            return 0.6
        else:
            return 0.3

    @property
    def acel_gravedad(self):
        return 0.6

    @property
    def velocidad_limite(self):
        if self.correr:
            return 3
        else:
            return 1.5

    @property
    def rozamiento(self):
        if self.correr:
            return 0.15
        else:
            return 0.075

    def sprint(self):
        if self.__en_suelo:
            self.correr = True

    def notsprint(self):
        self.correr = False

    # métodos para direcciones
    def direccion_right(self):
        "varía la direccion a la derecha"
        self.direccion += 1

    def direccion_left(self):
        "varía la dirección a la izq"
        self.direccion -= 1

    def direccion_reset(self):
        """resetea la dirección a 0"""
        self.direccion = 0

    def acelerar(self):
        """Varía la velocidad del jugador hasta un límite de 3px/s en la dirección especificada por el input"""
        # si la dirección es 0 significa que no hay input
        if self.direccion != 0 and abs(self.velocidad[0]) <= self.velocidad_limite:
            self.velocidad[0] += self.direccion * self.aceleracion

    def frenar(self):
        """aplica una fuerza de rozamiento sobre el jugador"""
        # si se mueve hacia la derecha
        if self.velocidad[0] > self.rozamiento:
            self.velocidad[0] -= self.rozamiento
        # si se mueve hacial a izquierda
        elif self.velocidad[0] < -1 * self.rozamiento:
            self.velocidad[0] += self.rozamiento
        # evitar errores decimales en el cerca del 0
        else:
            self.velocidad[0] = 0

    def movimiento(self):

        self.position[0] += self.velocidad[0]
        self.position[1] += self.velocidad[1]


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

    def gravedad(self):
        if not self.__en_suelo:
            self.velocidad[1] += self.acel_gravedad
            self.__frames_aire += 1

    def salto(self):
        """Establece una aceleración vertical durante un máximo de 7 frames en los que se mantenga pulsada la tecla
        correspondiente. Con esto permitimos que haya 7 alturas de salto dependiendo de cuánto se pulso el botón"""
        if self.__en_suelo or self.__frames_aire < 7:
            self.velocidad[1] -= 1.5

    """def animaciones(self):
        # si no está en el suelo ponme la skin de salto. Esto incluye si cae por un precipicio o una plataforma
        if not self.__en_suelo:
            self.sprite[1] = 48
            self.sprite[2] = 0
        else:
            # si no pon la skin base
            self.sprite[1] = 16
            self.sprite[2] = 0

            # si estamos en movimiento (esto harbría que cambiarlo según la dirección sea negativa o positiva para que
            # mario mire hacia el lado que debe) cambiame la skin. Más rápido cuánto más rápido me mueva
            if self.direccion != 0:
                Tenemos un segmento de módulo 45, creado por frame count % 45. Al dividirlo entre 15 estamos creando
                3 segmentos iguales de frames. Cada vez que cambie de segmento cambia de skin
                a = pyxel.frame_count % (45 / (int(self.velocidad[0]) + 1))
                if a // (15 / (int(self.velocidad[0]) + 1)) == 1:
                    self.sprite[1] = 32
                elif a // (15 / (int(self.velocidad[0]) + 1)) == 0:
                    self.sprite[1] = 16"""

    def update(self):
        self.acelerar()
        self.frenar()
        self.movimiento()
        self.gravedad()
        self.cuerpoTierra()
        #self.animaciones()

    def draw(self):
        pyxel.blt(self.position[0], self.position[1], *self.sprite, colkey=0)
        pyxel.text(0, 15, "%s\n%s, %s\n%i\n%s\n%s" % (
            self.position, self.velocidad[0], self.velocidad[1], self.__frames_aire, self.__en_suelo, self.sprite), 0)