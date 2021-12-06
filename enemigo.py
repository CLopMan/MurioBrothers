import pyxel

import constantes

from entidad import Entidad


class Enemigo():
    def __init__(self, x, y, suelo, sprite):
        self.position: list = [x, y]
        self.suelo: bool = suelo
        self.sprite: tuple = sprite
        self.velocidad: list = [0, 0]
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

    """@property
    def size(self):
        if self.sprite == constantes.SPRITE_KOOPA:
            a = (16, 24)
        elif self.sprite == constantes.SPRITE_GOOMBA:
            a = (16, 16)"""

    # Funciones
    def cuerpoTierra(self):
        """gravedad"""
        # temporalmente el suelo está en 208, si se pasa hacia abajo corrige el error
        if self.position[1] > self.suelo:
            # velocidad vertical = 0
            self.velocidad[1] = 0
            # corrige la posición
            self.position[1] = self.suelo

        elif self.position[1] < self.suelo - 2:
            self.velocidad[1] += constantes.GRAVEDAD
            self.position[1] += self.velocidad[1]
        else:
            self.position[1] = self.suelo

    def cambioDir(self):
        self.direccion *= -1

    def move(self, valor):
        self.position[0] += self.direccion * constantes.VELOCIDAD_ENEMIGOS - valor

    def clearAlturas(self):
        """Vacía el parámetros de las posibles alturas en las que mario se puede posar"""
        self.trues_alturas = list()

    def colisionBloque(self, boolList: list):
        """esta función recibe la lista de booleanos de la función colisión de los bloques y actúa en consecuencia"""
        # COLISIÓN VERTICAL POR ARRIBA
        # inmediatamente encima
        if boolList[1] and boolList[2]:
            if boolList[4] not in self.trues_alturas:
                self.trues_alturas.append(boolList[4])
        # derecha
        if not boolList[0] and not boolList[1]:
            self.clearAlturas()
            if self.sprite == constantes.SPRITE_GOOMBA:
                self.suelo = 208
            elif self.sprite == constantes.SPRITE_KOOPA:
                self.suelo = 200
        # izquierda (se ponen derecha e izquierda por separado para que no interactúen mal entre bloques)
        elif boolList[0]:
            if self.sprite == constantes.SPRITE_GOOMBA:
                self.suelo = 208
            elif self.sprite == constantes.SPRITE_KOOPA:
                self.suelo = 200

        # En caso de que haya varias alturas posibles, cogemos la más cercana
        if len(self.trues_alturas) > 0:
            min = self.trues_alturas[0]
            # para todas las alturas, saca la más cercana a mario
            for ii in self.trues_alturas:
                if ii < min:
                    min = ii
            self.suelo = min

        # Colisión lateral
        if boolList[1] and (not boolList[2] and not boolList[3]):
            # Cambia la dirección
            self.direccion *= -1

    # if self.sprite == constantes.SPRITE_KOOPA:
    # print(boolList)
    # Borrar si funciona colisionMario2
    """def colisionMario(self, other):
        Función que detecta si mario ha chocado horizontalmennte o verticalmente con un enemigo. aux[1] = True =>
        Mario chocó en la horizontal, aux[1] = True => mario chocó en la vertical
        aux = [False, False]
        # Mario está dentro del enemigo
        # debug: print(abs(self.position[1] - other.position[1]), self.size[1], other.size[1])
        if abs(self.position[0] - other.position[0]) < 16:
            aux[0] = True
        if other.size[1] > self.position[1] - other.position[1] >= 0 or 0 > self.position[1] - other.position[1] >-1*\
                self.size[1]:
            aux[1] = True
        return aux"""

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

    def draw(self):
        pyxel.blt(self.position[0], self.position[1], *self.sprite, colkey=10)
        pyxel.text(0, 216, "%s" % self.size, 0)

    def update(self):
        self.cuerpoTierra()
        self.clearAlturas()
