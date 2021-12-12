import pyxel
import constantes


class Enemigo:
    """Enemigos que aparecen a lo largo del nivel"""
    def __init__(self, x, y, suelo, sprite):
        # Posición y velocidad de los enemigos
        self.position: list = [x, y]
        self.velocidad: list = [constantes.VELOCIDAD_ENEMIGOS, 0]
        # Suelo del enemigo y altura
        self.suelo: int = suelo
        self.__trues_alturas: list = []
        # Sprite del enemigo
        self.sprite: tuple = sprite
        # Dirección
        self.__direccion: int = -1
        # Tamaño de enemigos
        self.size = constantes.TAMANNO_ENEMIGOS

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
        """esta función controla que el enemigo esté pisando el __suelo"""
        # Si el enemigo está por debajo del suelo
        if self.position[1] > self.suelo:
            # Velocidad vertical = 0
            self.velocidad[1] = 0
            # Corrige la posición
            self.position[1] = self.suelo
        # Si el enemigo está por encima del suelo
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
        # Se le suma la velocidad del enemigo menos la de la cámara
        self.position[0] += self.__direccion * self.velocidad[0] - valor

    def clearAlturas(self):
        """Vacía el parámetros de las posibles alturas en las que mario se puede posar"""
        self.__trues_alturas = list()

    def colisionBloque(self, boolList: list):
        """Esta función recibe la lista de booleanos de la función colisión de los bloques y actúa en consecuencia"""
        # COLISIÓN VERTICAL POR ARRIBA
        # Inmediatamente encima
        if boolList[1] and boolList[2]:
            if boolList[4] not in self.__trues_alturas:
                self.__trues_alturas.append(boolList[4])
        # Derecha
        if not boolList[0] and not boolList[1]:
            self.clearAlturas()
            self.suelo = 208
        # Izquierda (se ponen derecha e izquierda por separado para que no interactúen mal entre bloques)
        elif boolList[0]:
            self.suelo = 208
        # En caso de que haya varias alturas posibles, cogemos la más cercana al enemigo
        if len(self.__trues_alturas) > 0:
            min = self.__trues_alturas[0]
            # Para todas las alturas, saca la más cercana a mario
            for ii in self.__trues_alturas:
                if ii < min:
                    min = ii
            self.suelo = min
        # Colisión lateral
        if boolList[1] and (not boolList[2] and not boolList[3]):
            # Colisión derecha
            if -16 < boolList[5] - self.position[0] < 0:
                # Te mueve a la derecha
                self.position[0] = boolList[5] + 16
            # Colisión izquierda
            elif 0 < boolList[5] - self.position[0] < 16:
                # Te mueve a la izquierda
                self.position[0] = boolList[5] - 16
            # Cambia la dirección
            self.cambioDir()

    def animacionCaminar(self):
        if self.sprite == constantes.SPRITE_GOOMBA or self.sprite == constantes.SPRITE_GOOMBA_2:
            self.sprite = constantes.SPRITE_GOOMBA
            # Cada periodo de 5 frames cambia de sprite
            if pyxel.frame_count % 10 < 5:
                self.sprite = constantes.SPRITE_GOOMBA_2
        if self.sprite == constantes.SPRITE_KOOPA or self.sprite == constantes. SPRITE_KOOPA_2:
            # Comprueba la dirección
            if self.__direccion == 1:
                self.sprite = constantes.SPRITE_KOOPA
            else:
                self.sprite = constantes.SPRITE_KOOPA_2
                
    def update(self):
        """Update enemigo"""
        self.animacionCaminar()
        self.cuerpoTierra()

    def draw(self):
        """Dibujo enemigo"""
        # corrección de posición para que el dibujo quede bien
        if self.sprite == constantes.SPRITE_KOOPA or self.sprite == constantes.SPRITE_KOOPA_2:
            pyxel.blt(self.position[0], self.position[1] - 8, *self.sprite, colkey=10)
        else:
            pyxel.blt(self.position[0], self.position[1], *self.sprite, colkey=10)
