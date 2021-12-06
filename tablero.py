import pyxel
import constantes
from interfaz import Interfaz
from mario import Mario
from enemigo import Enemigo
from bloque import Bloque
from random import randint
from random import random


class Tablero:
    def __init__(self, w, h, velocidad, x):
        self.w: int = w
        self.h: int = h
        # posición en x de la cámara
        self.x: float = x
        self.velocidad: float = velocidad
        self.interfaz: Interfaz = Interfaz(0, 500, 0, 1, 1, 3)
        # Lista de enemigos, de momento sólo he metido y colocado el primero
        self.enemigos: list = []
        self.bloques: list = []
        for _ in constantes.POSICION_BLOQUES:
            self.bloques.append(Bloque(*_))
        self.mario: Mario = Mario(*constantes.POSICION_INICIAL_M)

    def move(self):
        """movimiento de la camara. Si mario llega al límite de la pantalla se queda inmovil y se mueve el mapa con
        la misma velocidad"""
        if self.x > -1784:
            moverpx = 0
            if self.mario.position[0] > 112:
                self.mario.position[0] = 112
                moverpx = self.mario.velocidad[0]
            self.x -= moverpx
            # si se mueve el escenario también se mueven los bloques
            for bloque in (self.bloques):
                bloque.move(moverpx)
            for enemigo in self.enemigos:
                enemigo.move(moverpx)
        else:
            self.x = -1784

    def inputs(self):
        """Recoge los distintas entradas del jugador"""
        # direccion = 0
        self.mario.direccion_reset()
        # correr
        if pyxel.btn(pyxel.KEY_X):
            self.mario.sprint()
        else:
            self.mario.notsprint()
        # izquierda
        if pyxel.btn(pyxel.KEY_LEFT):
            self.mario.direccion_left()
        # derecha
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.mario.direccion_right()
        # salto
        if pyxel.btn(pyxel.KEY_Z):
            self.mario.salto()

    def generarEnemigo(self):
        lista = []
        if len(self.enemigos) < 4:
            # Genera un enemigo (25% koopa 75% goomba)
            a = random()
            b = constantes.SPRITE_GOOMBA
            if a <= 0.25:
                b = constantes.SPRITE_KOOPA
            # Genera una y random
            y = randint(0, 12)
            x = 256
            # Comprueba que no esté dentro de un bloque
            for bloque in self.bloques:
                while abs(bloque.x - x) <= 16:
                    x += 16
                    
            self.enemigos.append(Enemigo(x, 16 * y, 200, b))


    def borrarEnemigo(self):
        for enemigo in self.enemigos:
            if enemigo.position[0] < - 100 or enemigo.position[1] > 240:
                self.enemigos.remove(enemigo)


    def update(self):
        """Ejecuta todas las interacciones entre objetos y el mapa"""
        self.interfaz.update()
        # Generar y borrar enemigo
        self.generarEnemigo()
        self.borrarEnemigo()
        # Colisiones entre Mario y enemigos con bloques
        for bloque in self.bloques:
            bloque.colision(self.mario)
            self.mario.colisionBloque(bloque.colision2(self.mario))
            for enemigo in self.enemigos:
                enemigo.colisionBloque(bloque.colision2(enemigo))
                enemigo.colisionMario2(self.mario)
                # print(enemigo.colisionMario2(self.mario))
                enemigo.update()
        # update estado de mario
        self.mario.update()
        # movimiento del mapa
        self.move()

    def draw(self):
        pyxel.bltm(self.x, 0, 0, 0, 32, 256, 256)
        self.interfaz.draw()
        self.mario.draw()
        for enemigo in self.enemigos:
            enemigo.draw()
        pyxel.text(122, 5, str(self.x), 7)
        # Bucle que dibuja los bloques rompibles (no fijarse en el tilemap- es una ref más o menos exacta del og)
        for bloque in self.bloques:
            bloque.draw()
