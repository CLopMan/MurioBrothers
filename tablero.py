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
        self.monedas: list = []
        # Lista de bloues, en el módulo de constantes están los datos para inicializar
        for _ in constantes.POSICION_BLOQUES:
            self.bloques.append(Bloque(*_))
        # Lista de monedas que que aparecen en el mapa
        self.mario: Mario = Mario(*constantes.POSICION_INICIAL_M)

    def move(self):
        """movimiento de la camara. Si mario llega al límite de la pantalla se queda inmovil y se mueve el mapa con
        la misma velocidad"""
        # límite del mapa
        if self.x > -1784:
            # scroll junto con todos los elemntos dibujados en él
            moverpx = 0
            if self.mario.position[0] > 112:
                self.mario.position[0] = 112
                moverpx = self.mario.velocidad[0]
            self.x -= moverpx
            # si se mueve el escenario también se mueven los bloques y enemigos
            for bloque in (self.bloques):
                bloque.move(moverpx)
            for enemigo in self.enemigos:
                enemigo.move(moverpx)
        else:
            self.x = -1784

    def inputs(self):
        """Recoge los distintas entradas del jugador"""
        # __direccion = 0
        self.mario.direccion_reset()
        # imput para __correr
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
        # reinicio del nivel
        if pyxel.btnp(pyxel.KEY_R):
            self.reiniciar()
        # debug de los enemigos
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.enemigos.clear()

    def generarEnemigo(self):
        """Función encargada de generar enemigos con un límite de 4 a la vez en la pantalla"""
        i = randint(1, 10)
        if pyxel.frame_count % i == 0:
            # Genera un enemigo (25% koopa 75% goomba)
            a = random()
            b = constantes.SPRITE_GOOMBA
            if a <= 0.25:
                b = constantes.SPRITE_KOOPA
            # Genera una y y una x random
            y = 208
            x = randint(0, 4)
            # comprobamos que el enemigo no esté dentro de un bloque
            for bloque in self.bloques:
                while abs(bloque.x - x) < 16 and -16 < bloque.y - y < b[-1]:
                    x += 16
            if len(self.enemigos) < 4:
                # añadir enemigo a la lista con posición fuera de los límites de la cámara hacia la derecha
                self.enemigos.append(Enemigo(256 + (16 * x), y, 200, b))

    def borrarEnemigo(self):
        """Función encargada de eliminar un enemigo si este se sale por la izquierda"""
        for enemigo in self.enemigos:
            if enemigo.position[0] < -16 or enemigo.position[1] >= 256:
                self.enemigos.remove(enemigo)

    def reiniciar(self):
        """Reinicio del nivel"""
        self.__init__(constantes.WIDTH, constantes.HEIGHT, constantes.VELOCIDAD, constantes.X)

    def borrarBloque(self, bloque):
        """Función encargada de borrar bloques que se salen por la izquierda"""
        if bloque.x < - 16:
            self.bloques.remove(bloque)

    def interaccionMarioBloque(self, bloque):
        """Función que aplica la transformación adecuada a un bloque según su interación con mario"""
        if bloque.sprite == constantes.SPRITE_BLOQUE and self.mario.estado >= 0:
            self.bloques.remove(bloque)
        if bloque.sprite == constantes.SPRITE_INTERR:
            bloque.cambioBloqueLiso()

    def update(self):
        """Ejecuta todos los métodos en el orden correcto"""
        # Interfaz (tiempo, monedas, vidas...)
        self.interfaz.update()

        # Generar enemigos
        if pyxel.frame_count % 30 == 0:
            self.generarEnemigo()

        # == bucles de bloques y enemigos ==
        for bloque in self.bloques:
            # colisión mario-bloque
            if self.mario.colisionBloque(bloque.colision2(self.mario)):
                self.interaccionMarioBloque(bloque)
            # si el bloque se sale de escena
            self.borrarBloque(bloque)
            # interacción con enemigos
            for enemigo in self.enemigos:
                # colisión enemigo-bloque
                enemigo.colisionBloque(bloque.colision2(enemigo))
        # == bucle de monedas ==

        # Update de enemigo (debe ir en un bucle separado porque el anterior hizo todos los cálculos necesarios para el
        # enemigo: colisiones, __suelo. Esta función ahora se encarga de trabajar con esos datos)
        for enemigo in self.enemigos:
            enemigo.update()
        # Tras haber hecho las operaciones correspondientes con cada enemigo, se pude borrar? Función encargada de eso
        self.borrarEnemigo()
        # update estado de mario
        self.mario.update()
        # scroll (movimiento del mapa y lo que está dibujado encima)
        self.move()

    def draw(self):
        """Función encargada de dibujar el mapa y lo demás encima"""
        # fondo
        pyxel.bltm(self.x, 0, 0, 0, 32, 256, 256)
        # Interfaz
        self.interfaz.draw()
        # Mario
        self.mario.draw()
        # Enemigos
        for enemigo in self.enemigos:
            enemigo.draw()
        # bloques
        for bloque in self.bloques:
            bloque.draw()