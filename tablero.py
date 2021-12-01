import pyxel
import constantes
from interfaz import Interfaz
from mario import Mario
from enemigo import Enemigo


class Tablero:
    def __init__(self, w, h, velocidad, x):
        self.w: int = w
        self.h: int = h
        # posición en x de la cámara
        self.x: float = x
        self.velocidad: float = velocidad

        self.interfaz: Interfaz = Interfaz(0, 999, 0, 1, 1, 3)
        # Lista de enemigos, de momento sólo he metido y colocado el primero
        self.enemigos: list = [Enemigo(*constantes.ENEMIGOS_XY[0])]
        self.bloques: list = []
        self.mario: Mario = Mario(*constantes.POSICION_INICIAL_M)

    def move(self):
        """movimiento de la camara. Si mario llega al límite de la pantalla se queda inmovil y se mueve el mapa con
        la misma velocidad"""
        moverpx = 0
        if self.mario.position[0] > 112:
            self.mario.position[0] = 112
            moverpx = self.mario.velocidad[0]
        self.x -= moverpx

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
        # pequeño debug para comprobar que el goomba cambia bien de dirección. Borrar en un futuro para que esto
        # ocurra si se choca
        if pyxel.btnp(pyxel.KEY_D):
            self.enemigos[0].cambioDir()

    def update(self):
        """Ejecuta todas las interacciones entre objetos y el mapa"""
        self.mario.update()
        self.move()
        self.enemigos[0].move()
        self.enemigos[0].cuerpoTierra()

    def draw(self):
        pyxel.bltm(self.x, 0, 0, 0, 32, 256, 256)
        pyxel.text(60, 0, str(self.mario.position), 7)
        self.interfaz.draw()
        self.mario.draw()
        self.enemigos[0].draw()
        # Mirar. Bucle que dibuja los bloques pero está jodido
        for i in range(len(constantes.POSICION_BLOQUES)):
            pyxel.blt(constantes.POSICION_BLOQUES[i][0] * 8 + self.x, constantes.POSICION_BLOQUES[i][1] + 122, 0, 32,
                      16, 16, 16)
