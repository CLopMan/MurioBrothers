import pyxel
import constantes


class Objeto:
    def __init__(self, x: float, y: float, sprite: tuple, suelo):
        """Inicialización de objetos
        @param x: coordenada en x
        @ param y: coordenada en y
        @param sprite: dibujo
        @param suelo: límite en y al que el objeto puede caer
        """
        # Posición
        self.position: list = [x, y]
        # Velocidad
        self.velocidad: list = [constantes.VELOCIDAD_OBJETO, 0]
        # tamaño de la hitbox
        self.size: list = [16, 16]
        # sentido del movimiento
        self.__dir: int = 1
        # sprite
        self.sprite: tuple = sprite
        # suelo
        self.__suelo: int = suelo
        # lista de posibles suelos de objeto
        self.__trues_alturas = list()

    # MÉTODOS DE MOVIMIENTO
    def cuerpoTierra(self):
        """esta función controla que el jugador esté pisando el __suelo"""
        if self.position[1] > self.__suelo:
            # velocidad vertical = 0
            self.velocidad[1] = 0
            # corrige la posición
            self.position[1] = self.__suelo

        elif self.position[1] < self.__suelo:
            self.velocidad[1] += constantes.GRAVEDAD
            self.position[1] += self.velocidad[1]
        else:
            self.position[1] = self.__suelo

    def move(self, valor):
        """Movimiento horizontal"""
        self.position[0] += self.__dir * self.velocidad[0] - valor

    # MÉTODOS DE COLISIONES
    def clearAlturas(self):
        """Vacía el parámetros de las posibles alturas en las que mario se puede posar"""
        self.__trues_alturas = list()

    def colisionBloque(self, boolList: list):
        """esta función recibe la lista de booleanos de la función colisión de los bloques y actúa en consecuencia"""
        # COLISIÓN VERTICAL POR ARRIBA
        # inmediatamente encima
        if boolList[1] and boolList[2]:
            if boolList[4] not in self.__trues_alturas:
                self.__trues_alturas.append(boolList[4])
        # derecha
        if not boolList[0] and not boolList[1]:
            self.clearAlturas()
            self.__suelo = 208
        # izquierda (se ponen derecha e izquierda por separado para que no interactúen mal entre bloques)
        elif boolList[0]:
            self.__suelo = 208

        # En caso de que haya varias alturas posibles, cogemos la más cercana al enemigo
        if len(self.__trues_alturas) > 0:
            min = self.__trues_alturas[0]
            # para todas las alturas, saca la más cercana a mario
            for ii in self.__trues_alturas:
                if ii < min:
                    min = ii
            self.__suelo = min

        # Colisión lateral
        if boolList[1] and (not boolList[2] and not boolList[3]):
            # colisión derecha
            if -16 < boolList[5] - self.position[0] < 0:
                # Te mueve a la derecha
                self.position[0] = boolList[5] + 16
            # colisión izquierda
            elif 0 < boolList[5] - self.position[0] < 16:
                # Te mueve a la izquierda
                self.position[0] = boolList[5] - 16
            # Cambia la dirección
            self.__dir *= -1

    # GENERAL
    def update(self):
        """Update funciones de los objetos"""
        self.cuerpoTierra()
        self.clearAlturas()

    def draw(self):
        """Dibuja los objeteos"""
        pyxel.blt(self.position[0], self.position[1], *self.sprite, colkey=12)