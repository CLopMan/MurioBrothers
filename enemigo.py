import pyxel

import constantes

from entidad import Entidad

class Enemigo():
    def __init__(self, x, y, suelo, sprite):
        self.position:list = [x, y]
        self.suelo:bool = suelo
        self.sprite:tuple = sprite
        self.velocidad:list = [0, 0]
        # dirección
        self.direccion:bool = -1
        self.trues_alturas: list = []
        self.size: list = [16, 16]

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
        control = True
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

        # En caso de que haya varias alturas posibles, cogemos la más cercana a mario
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

    def draw(self):
        pyxel.blt(self.position[0], self.position[1], *self.sprite, colkey=10)

    def update(self):
        self.move(0)
        self.cuerpoTierra()
        self.clearAlturas()