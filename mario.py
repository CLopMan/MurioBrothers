import pyxel


class Mario:
    """personaje principal, conjunto de todos los parámetros necesiarios"""

    def __init__(self):
        # posición x e y
        self.position: list = [5.0, 200.0]
        # velocidad en x e y
        self.velocidad: list = [0.0, 0.0]
        # direccion (1 = derecha, -1 = izquierda)
        self.direccion = 0
        # sprintar
        self.correr = False
        # control de sprite
        self.sprite: list = [0, 0, 0, 16, 16]
        # está en el suelo?
        self.en_suelo = False

    @property
    def position(self) -> list:
        return self.__position
    @position.setter
    def position(self, lista):
        if type(lista) == list:
            if len(lista) == 2:
                if type(lista[0]) != float or type(lista[1]) != float:
                    raise TypeError("Elementos de position deben ser float o enteros")
                else:
                    self.__position = lista
            else:
                raise ValueError("position debe tener logitud 2")
        else:
            raise TypeError("Position debe ser una lista")

    @property
    def velocidad(self):
        Type

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
            return 6
        else:
            return 3

    @property
    def rozamiento(self):
        if self.en_suelo:
            return 0.1
        else:
            return 0.25

    def sprint(self):
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
