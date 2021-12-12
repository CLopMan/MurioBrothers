import pyxel
import constantes
from objetos import Objeto

class Mario:
    """Personaje principal, conjunto de todos los parámetros necesiarios"""

    def __init__(self, x, y, suelo, size, sprite):
        # posición x e y
        self.position: list = [x, y]
        # Suelo de Mario
        self.__suelo: int = suelo
        # ancho y alto
        self.size: list = size
        # sprite de mario
        self.sprite: list = sprite
        # velocidad en x e y
        self.velocidad: list = [0.0, 0.0]
        # __direccion (1 = derecha, -1 = izquierda)
        self.__direccion: int = 0
        # estado de mario (si es grande, pequeño, flor de fuego o estrella)
        self.estado: int = 0
        # DISPARADORES DE CIERTAS ACCIONES DE MOVIMEINTO
        # disparador sprintar
        self.__correr: bool = False
        # disparador de salto
        self.__saltar: bool = False
        # PARÁMETROS DE CONTROL SOBRE ALGUNAS FUNCIONES
        # contador de frames en el aire
        self.__frames_aire: int = 0
        # conteo de los frames desde la última colisión
        self.__frames_desde_colision: int = 90
        # comprobación de que mario está en el __suelo
        self.__en_suelo: bool = True
        # Posibles suelos de mario
        self.__trues_alturas: list = list()

    # Atributos de sólo lectura:
    @property
    def aceleracion(self):
        if self.__correr:
            return constantes.ACELERACION[1]
        else:
            return constantes.ACELERACION[0]

    @property
    def acel_gravedad(self):
        return constantes.GRAVEDAD

    @property
    def velocidad_limite(self):
        if self.__correr:
            return constantes.VELOCIDAD_LIMITE[1]
        else:
            return constantes.VELOCIDAD_LIMITE[0]

    @property
    def rozamiento(self):
        if self.__correr:
            return constantes.ROZAMIENTO[1]
        else:
            return constantes.ROZAMIENTO[0]

    # Funciones del movimiento

    def sprint(self):
        """Disparador de la función __correr"""
        if self.__en_suelo:
            self.__correr = True

    def notsprint(self):
        """Desactivar __correr"""
        self.__correr = False

    # Métodos para direcciones. Se usan sumas para que puedas pulsar varios botones a la vez y te quedes quieto
    def direccion_right(self):
        """Cambia la __direccion hacia la derecha"""
        # sprite para frenar
        if self.velocidad[0] < 0:
            self.sprite[2] = 0
        self.__direccion += 1

    def direccion_left(self):
        """varía la dirección a la izquierda"""
        # sprite para frenar
        if self.velocidad[0] > 0:
            self.sprite[2] = 0
        self.__direccion -= 1

    def direccion_reset(self):
        """Resetea la dirección a 0"""
        self.__direccion = 0

    def acelerar(self):
        """Varía la velocidad del jugador hasta un límite de 3px/s en la dirección especificada por el input"""
        # Si la dirección es 0 significa que no hay input
        if self.__direccion != 0 and abs(self.velocidad[0]) <= self.velocidad_limite:
            self.velocidad[0] += self.__direccion * self.aceleracion

    def frenar(self):
        """Aplica una fuerza de rozamiento sobre el jugador"""
        # Si se mueve hacia la derecha
        if self.velocidad[0] > self.rozamiento:
            self.velocidad[0] -= self.rozamiento
        # Si se mueve hacial a izquierda
        elif self.velocidad[0] < -1 * self.rozamiento:
            self.velocidad[0] += self.rozamiento
        # Evitar errores decimales cerca del 0
        else:
            self.velocidad[0] = 0

    def movimiento(self):
        """Funcion que actualiza la posición de mario en función de la velocidad"""
        # Comprobación del borde izquierdo
        if 240 >= self.position[0] > 0:
            self.position[0] += self.velocidad[0]
        # Evita que Mario se salga por la pantalla
        elif self.position[0] > 240:
            self.position[0] = 240
            self.velocidad[0] = 0
        else:
            self.position[0] = 0.1
            self.velocidad[0] = 0
        self.position[1] += self.velocidad[1]

    def conteoFrames(self):
        """Cuenta los frames que mario ha estado en el aire"""
        if not self.__en_suelo:
            self.__frames_aire += 1
        else:
            self.__frames_aire = 0

    def cuerpoTierra(self):
        """esta función controla que el jugador esté pisando el __suelo"""
        # Si se pasa hacia abajo corrige el error
        if self.position[1] > self.__suelo:
            self.__en_suelo = True
            # Resetea el valor de frames en el aire
            # Velocidad vertical = 0
            self.velocidad[1] = 0
            # Corrige la posición
            self.position[1] = self.__suelo
        elif self.position[1] < self.__suelo:
            self.__en_suelo = False

    def gravedad(self):
        """Aplica una aceleración hacia abajo si mario se despega del __suelo"""
        if not self.__en_suelo:
            self.velocidad[1] += self.acel_gravedad

    def salto(self):
        """Establece una aceleración vertical durante un máximo de 7 frames en los que se mantenga pulsada la tecla
        correspondiente. Con esto permitimos que haya 7 alturas de salto dependiendo de cuánto se pulso el botón"""
        if self.__en_suelo or self.__frames_aire < 4:
            if self.estado <= 0:
                self.velocidad[1] -= 2
            elif self.estado > 0:
                self.velocidad[1] -= 2.25

    def controlSprite(self):
        """Controla el sprite de Mario en función a su estado"""
        if self.estado >= 1:
            self.sprite[4] = 32
        elif self.estado < 1:
            self.sprite[4] = 16

    def animacionCaminar(self):
        """Controla los sprites de mario en los movimientos básicos, los sprites están organizados por columnas. Las
        funciones de dirección establecen qué columna usamos y esta función define cual de las skins"""
        # Multiplicador para aplicar los números correctos según sea grande o pequeño
        i = 1
        if self.estado >= 1:
            i = 2
        # Sprites para mirar a la derecha o la izquierda
        # Derecha
        if self.__direccion == 1:
            if self.estado == 0:
                self.sprite[1] = 64
            elif self.estado == 1:
                self.sprite[1] = 96
        # Izquierda
        elif self.__direccion == -1:
            if self.estado == 0:
                self.sprite[1] = 80
            elif self.estado == 1:
                self.sprite[1] = 112
        # Animación de caminar
        # Pasos. Si la velocidad y la dirección son en sentidos contrario se pone el sprite de
        # frenar (métodos de direccion)
        if self.__en_suelo and self.__direccion * self.velocidad[0] >= 0:
            self.sprite[2] = 16 * i
            if self.velocidad[0] != 0:
                # Cada periodo de 5 frames cambia de sprite
                if pyxel.frame_count % 10 < 5:
                    self.sprite[2] = 32 * i
            # Parado
            else:
                self.sprite[2] = 16 * i
        # Si está en el aire salta
        elif not self.__en_suelo:
            self.sprite[2] = 48 * i

    def clearAlturas(self):
        """Vacía el parámetros de las posibles alturas en las que mario se puede posar"""
        self.__trues_alturas.clear()

    def colisionBloque(self, boolList: list):
        """Esta función recibe la lista de booleanos de la función colisión de los bloques y actúa en consecuencia
        Si ha colisionado por abajo devuelve un booleano que el método interaccionMarioBloque de tablero usará para
        aplicar las transformaciones adecuadas a los bloques"""
        # Suelo por defecto
        if self.estado >= 1:
            defecto = 192
        else:
            defecto = 208
        # COLISIÓN VERTICAL POR ARRIBA
        # Inmediatamente encima
        control = True
        if boolList[1] and boolList[2]:
            if boolList[4] not in self.__trues_alturas:
                self.__trues_alturas.append(boolList[4])
        # Derecha
        if not boolList[0] and not boolList[1]:
            self.clearAlturas()
            self.__suelo = defecto
        # Izquierda (se ponen derecha e izquierda por separado para que no interactúen mal entre bloques)
        elif boolList[0]:
            self.__suelo = defecto
        # En caso de que haya varias alturas posibles, cogemos la más cercana a mario
        if len(self.__trues_alturas) > 0:
            min = self.__trues_alturas[0]
            # Para todas las alturas, saca la más cercana a mario
            for ii in self.__trues_alturas:
                if ii < min:
                    min = ii
            self.__suelo = min
        # Debajo (si está inmediatamente debajo)
        if boolList[1]:
            if self.velocidad[1] < 0 and 0 > (boolList[4] - self.position[1]) > -16:
                self.velocidad[1] = 0
                self.position[1] = boolList[4] + 16
                control = False
                return True
        # COLISIÓN LATERAL
        if control:
            if boolList[1] and (not boolList[2] and not boolList[3]):
                # Colisión derecha
                if -16 < boolList[5] - self.position[0] < 0:
                    # Te mueve a la derecha
                    self.velocidad[0] = 0
                    self.position[0] = boolList[5] + 16
                # Colisión izquierda
                elif 0 < boolList[5] - self.position[0] < 16:
                    # Te mueve a la izquierda
                    self.velocidad[0] = 0
                    self.position[0] = boolList[5] - 16
                return False

    def colisionEntidad(self, other):
        """Función que detecta si Mario ha colisionado con un enemigo, en caso afirmativo comprueba si mario ha
        colisionado por arriba, aux[0] evalúa si han colisionado, aux[1] evalúa si mario viene de arriba"""
        aux = [False, False]
        # Si el sprite de Mario se superpone con otro sprite de enemigo u objeto
        if abs(other.position[0] - self.position[0]) < 16 and (
                self.size[1] > other.position[1] - self.position[1] >= 0 or 0 > other.position[1] - self.position[
            1] > -1 * other.size[1]):
            aux[0] = True
            # Si mario viene de arriba (aplicamos una correción de velocidad ya que la colisión no se activa hasta que
            # ambas entidades se superpongan)
            if self.velocidad[1] > 0 and self.position[1] < other.position[1] + self.velocidad[1]:
                aux[1] = True
        aux = tuple(aux)
        return aux

    def danno(self):
        """Hace daño a Mario si los frames de inencibilidad son menores a 90"""
        if self.__frames_desde_colision >= 90:
            # actualiza el sprite
            if self.estado >= 1:
                self.sprite[1] -= 32
            self.estado -= 1
            self.__frames_desde_colision = 0


    def dannont(self):
        """Aumenta el estado de Mario, la salud"""
        self.estado += 1
        # actualiza el sprite
        self.sprite[1] += 32

    def conteoFramesColision(self):
        """Cuenta los frames desde la última colisión para aplicar una cierta invulnerabilidad a Mario"""
        if self.__frames_desde_colision < 90:
            self.__frames_desde_colision += 1

    def rebote(self):
        """Aplica una pequeña velocidad hacia arriba para dar la ilusión de rebote"""
        self.velocidad[1] = -6

    def cambiarTamanio(self):
        """Cambia el tamaño de Mario según el estado de Mario"""
        if self.estado == 0:
            self.size = [16, 16]
        elif self.estado > 0:
            self.size = [16, 32]

    def update(self):
        """Ejecuta todas las funciones de mario en el orden adecuado para su funcionamiento"""
        self.acelerar()
        self.frenar()
        self.conteoFrames()
        self.animacionCaminar()
        self.movimiento()
        self.gravedad()
        self.conteoFramesColision()
        self.cambiarTamanio()
        self.controlSprite()
        self.cuerpoTierra()
        self.clearAlturas()

    def draw(self):
        """Dibuja a mario"""
        pyxel.blt(self.position[0], self.position[1], *self.sprite, colkey=0)

