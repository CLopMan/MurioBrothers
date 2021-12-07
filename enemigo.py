import pyxel

import constantes

class Enemigo():
    def __init__(self, x, y, suelo, sprite):
        self.position: list = [x, y]
        self.suelo: int = suelo
        self.sprite: tuple = sprite
        self.velocidad: list = [constantes.VELOCIDAD_ENEMIGOS, 0]
        # dirección
        self.direccion: int = -1
        self.trues_alturas: list = []
        self.size = [16, 16]

    # Properties
    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, valor):
        if type(valor) == list:
            self.__position = valor

    @property
    def velocidad(self):
        return self.__velocidad

    @velocidad.setter
    def velocidad(self, valor):
        if type(valor) == list:
            self.__velocidad = valor

    @property
    def sprite(self):
        return self.__sprite

    @sprite.setter
    def sprite(self, valor):
        if type(valor) == tuple:
            self.__sprite = valor

    # Funciones
    def cuerpoTierra(self):
        """esta función controla que el jugador esté pisando el suelo"""
        # temporalmente el suelo está en 208, si se pasa hacia abajo corrige el error
        if self.position[1] > self.suelo:
            # velocidad vertical = 0
            self.velocidad[1] = 0
            # corrige la posición
            self.position[1] = self.suelo
        elif self.position[1] < self.suelo:
            if self.velocidad[1] < constantes.LIM_VEL_VERT:
                self.velocidad[1] += constantes.GRAVEDAD
            else:
                self.velocidad[1] = constantes.LIM_VEL_VERT
            self.position[1] += self.velocidad[1]
        else:
            self.position[1] = self.suelo

    def cambioDir(self):
        """Cambia el sentido horizontal del movimiento"""
        self.direccion *= -1

    def move(self, valor):
        """Movimiento horizontal"""
        self.position[0] += self.direccion * self.velocidad[0] - valor

    def clearAlturas(self):
        """Vacía el parámetros de las posibles alturas en las que mario se puede posar"""
        self.trues_alturas = list()

    def colisionBloque(self, boolList: list):
        """esta función recibe la lista de booleanos de la función colisión de los bloques y actúa en consecuencia"""
        control = True
        # COLISIÓN VERTICAL POR ARRIBA
        # inmediatamente encima
        if boolList[1] and boolList[2]:
            if boolList[4] not in self.trues_alturas:
                self.trues_alturas.append(boolList[4])
        # derecha
        if not boolList[0] and not boolList[1]:
            self.clearAlturas()
            self.suelo = 208
        # izquierda (se ponen derecha e izquierda por separado para que no interactúen mal entre bloques)
        elif boolList[0]:
            self.suelo = 208

        # En caso de que haya varias alturas posibles, cogemos la más cercana al enemigo
        if len(self.trues_alturas) > 0:
            min = self.trues_alturas[0]
            # para todas las alturas, saca la más cercana a mario
            for ii in self.trues_alturas:
                if ii < min:
                    min = ii
            self.suelo = min

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
            self.cambioDir()

    def colisionMario2(self, other):
        """Función que detecta si Mario ha colisionado con un enemigo, en caso afirmativo comprueba si mario ha
        colisionado por arriba, aux[0] evalúa si han colisionado, aux[1] evalúa si mario viene de arriba"""
        aux = [False, False]
        if abs(self.position[0] - other.position[0]) < 16 and (
                other.size[1] > self.position[1] - other.position[1] >= 0 or 0 > self.position[1] - other.position[1] > -1 * self.size[1]):
            aux[0] = True
            # si mario viene de arriba (aplicamos una correción de velocidad ya que la colisión no se activa hasta que
            # ambas entidades se superpongan)
            if other.velocidad[1] > 0 and other.position[1] < self.position[1] + other.velocidad[1]:
                aux[1] = True
        aux = tuple(aux)
        return aux

    def update(self):
        """Update enemigo"""
        self.cuerpoTierra()

    def draw(self):
        """Dibujo enemigo"""
        # corrección de posición para que el dibujo quede bien
        if self.sprite == constantes.SPRITE_KOOPA:
            pyxel.blt(self.position[0], self.position[1] - 8, *self.sprite, colkey=10)
        else:
            pyxel.blt(self.position[0], self.position[1], *self.sprite, colkey=10)
        # Info de debug
        pyxel.text(0, 50, "%s\n%s, %s\n%s\n %s" % (self.position, self.velocidad[0], self.velocidad[1], self.trues_alturas, self.suelo), 0)
