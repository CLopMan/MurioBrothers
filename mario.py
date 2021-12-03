import pyxel
import constantes

class Mario():
    """personaje principal, conjunto de todos los parámetros necesiarios"""

    def __init__(self, x, y, suelo, size, sprite):
        # super().__init__(x, y, suelo, sprite)
        # Suelo de Mario
        self.suelo = suelo
        # ancho y alto
        self.size = size
        # sprite de mario
        self.sprite = sprite
        # posición x e y
        self.position: list = [x, y]
        # velocidad en x e y
        self.velocidad: list = [0.0, 0.0]
        # direccion (1 = derecha, -1 = izquierda)
        self.direccion = 0
        # sprintar
        self.correr = False
        # control de sprite
        self.sprite: list = [0, 64, 16, 16, 16]
        # disparador de salto
        self.__saltar = False
        # contador de frames en el aire
        self.__frames_aire = 0
        # comprobación de que mario está en el suelo
        self.__en_suelo = True

    # MOVIMIENTO

    # Atributos de sólo lectura:
    @property
    def aceleracion(self):
        if self.correr:
            return constantes.ACELERACION[1]
        else:
            return constantes.ACELERACION[0]

    @property
    def acel_gravedad(self):
        return constantes.GRAVEDAD

    @property
    def velocidad_limite(self):
        if self.correr:
            return constantes.VELOCIDAD_LIMITE[1]
        else:
            return constantes.VELOCIDAD_LIMITE[0]

    @property
    def rozamiento(self):
        if self.correr:
            return constantes.ROZAMIENTO[1]
        else:
            return constantes.ROZAMIENTO[0]

    # Funciones del movimiento

    def sprint(self):
        """Disparador de la función correr"""
        if self.__en_suelo:
            self.correr = True

    def notsprint(self):
        """Desactivar correr"""
        self.correr = False

    # métodos para direcciones. Se usan sumas para que puedas pulsar varios botones a la vez y te quedes quieto
    def direccion_right(self):
        """Cambia la direccion hacia la derecha"""
        self.sprite[1] = 64
        # sprite de frenado en caso de que vengamos de otra direccion
        if self.velocidad[0] < 0:
            self.sprite[2] = 0
        self.direccion += 1

    def direccion_left(self):
        """varía la dirección a la izquierda"""
        self.sprite[1] = 80
        # sprite de frenado si venimos de la otra direccion
        if self.velocidad[0] > 0:
            self.sprite[2] = 0
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
        """Funcion que actualiza la posición de mario en función de la velocidad"""
        # comprobación del borde izquierdo
        if self.position[0] > 0:
            self.position[0] += self.velocidad[0]
        else:
            self.position[0] = 0.1
            self.velocidad[0] = 0
        self.position[1] += self.velocidad[1]

    def conteoFrames(self):
        if not self.__en_suelo:
            self.__frames_aire += 1
        else:
            self.__frames_aire = 0

    def cuerpoTierra(self):
        """esta función controla que el jugador esté pisando el suelo, si no lo está pisando cuenta los frames que está
        en el aire"""
        # temporalmente el suelo está en 208, si se pasa hacia abajo corrige el error
        if self.position[1] > 208:
            self.__en_suelo = True
            # resetea el valor de frames en el aire
            # velocidad vertical = 0
            self.velocidad[1] = 0
            # corrige la posición
            self.position[1] = 208
        elif self.position[1] < 208:
            self.__en_suelo = False
            # si se despega del suelo cuenta los frames que esté ne el aire

    def gravedad(self):
        """Aplica una aceleración hacia abajo si mario se despega del suelo"""
        if not self.__en_suelo:
            self.velocidad[1] += self.acel_gravedad

    def salto(self):
        """Establece una aceleración vertical durante un máximo de 7 frames en los que se mantenga pulsada la tecla
        correspondiente. Con esto permitimos que haya 7 alturas de salto dependiendo de cuánto se pulso el botón"""
        if self.__en_suelo or self.__frames_aire < 7:
            self.velocidad[1] -= 1.5

    def animacionCaminar(self):
        """Controla los sprites de mario en los movimientos básicos, los sprites están organizados por columnas. Las
        funciones de dirección establecen qué columna usamos y esta función define cual de las skins"""
        # animación de caminar si está en el suelo y la dirección y el sentido de la velocidad coinciden. Si no
        # coinciden significa que todavía se está ejecutando el freno activo (skin propia)
        if self.__en_suelo and self.direccion * self.velocidad[0] >= 0:
            self.sprite[2] = 16
            if self.velocidad[0] != 0:
                # cada periodo de 5 frames cambia de sprite
                if pyxel.frame_count % 10 < 5:
                    self.sprite[2] = 32
            # parado
            else:
                self.sprite[2] = 16
        # si está en el aire salta
        elif not self.__en_suelo:
            self.sprite[2] = 48

    def update(self):
        """Ejecuta todas las funciones de mario en el orden adecuado para su funcionamiento"""
        self.acelerar()
        self.frenar()
        self.conteoFrames()
        self.animacionCaminar()
        self.movimiento()
        self.gravedad()
        self.cuerpoTierra()

    def draw(self):
        """Dibuja a mario"""
        pyxel.blt(self.position[0], self.position[1], *self.sprite, colkey=0)
        # menú debug
        pyxel.text(0, 15, "%s\n%s, %s\n%i\n%s\n%s" % (
            self.position, self.velocidad[0], self.velocidad[1], self.__frames_aire, self.__en_suelo, self.sprite), 0)
