import pyxel

import constantes


class Enemigo:
    """Enemigos que aparecen a lo largo del nivel"""
    def __init__(self, x, y, suelo, sprite):
        self.position: list = [x, y]
        self.suelo: int = suelo
        self.sprite: tuple = sprite
        self.velocidad: list = [constantes.VELOCIDAD_ENEMIGOS, 0]
        # dirección
        self.__direccion: int = -1
        self.__trues_alturas: list = []
        self.size: list = [16, 16]

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
        """esta función controla que el jugador esté pisando el __suelo"""
        if self.position[1] > self.suelo:
            # velocidad vertical = 0
            self.velocidad[1] = 0
            # corrige la posición
            self.position[1] = self.suelo

        elif self.position[1] < self.suelo:
            self.velocidad[1] += constantes.GRAVEDAD
            self.position[1] += self.velocidad[1]
        else:
            self.position[1] = self.suelo

    def cambioDir(self):
        """Cambia el sentido horizontal del movimiento"""
        self.__direccion *= -1

    def move(self, valor):
        """Movimiento horizontal"""
        self.position[0] += self.__direccion * self.velocidad[0] - valor


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
            self.suelo = 208
        # izquierda (se ponen derecha e izquierda por separado para que no interactúen mal entre bloques)
        elif boolList[0]:
            self.suelo = 208

        # En caso de que haya varias alturas posibles, cogemos la más cercana al enemigo
        if len(self.__trues_alturas) > 0:
            min = self.__trues_alturas[0]
            # para todas las alturas, saca la más cercana a mario
            for ii in self.__trues_alturas:
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

    def movimientoCaparazon(self):
        if self.__direccion == 0:
            self.__direccion = 1
        else:
            self.__direccion = 0


    def animacionCaminar(self):
        if self.sprite == constantes.SPRITE_GOOMBA or self.sprite == constantes.SPRITE_GOOMBA_2:
            self.sprite = constantes.SPRITE_GOOMBA
            # cada periodo de 5 frames cambia de sprite
            if pyxel.frame_count % 10 < 5:
                self.sprite = constantes.SPRITE_GOOMBA_2

    def update(self):
        """Update enemigo"""
        self.animacionCaminar()
        self.cuerpoTierra()

    def draw(self):
        """Dibujo enemigo"""
        # corrección de posición para que el dibujo quede bien
        if self.sprite == constantes.SPRITE_KOOPA:
            pyxel.blt(self.position[0], self.position[1] - 8, *self.sprite, colkey=10)
        else:
            pyxel.blt(self.position[0], self.position[1], *self.sprite, colkey=10)
        # Info de debug
        pyxel.text(0, 50, "%s\n%s, %s\n%s\n %s" % (
            self.position, self.velocidad[0], self.velocidad[1], self.__trues_alturas, self.suelo), 0)
