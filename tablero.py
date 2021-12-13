import pyxel
import constantes
from interfaz import Interfaz
from mario import Mario
from enemigo import Enemigo
from bloque import Bloque
from random import randint
from random import random
from objetos import Objeto


class Tablero:
    """Este módulo recoge lo que ha de ser colocado en pantalla, así como la interacción entre objetos y la lógica del
    juego"""

    def __init__(self, w: int, h: int, x: float, intentos: int):
        """Función para inicializar el tablero.
        @param w: ancho de la pantalla
        @param h: alto de la pantalla
        @param velocidad: velocidad de movimiento de la cámara
        @param x: posición del mapa
        @param intentos: entero que controla el número de veces que se ha reiniciado el nivel. Sirve para las vidas
        """
        # Atributo que controla el número de intentos del nivel
        self.intentos = 0 + intentos
        # Ancho y alto de la pantalla
        self.w: int = w
        self.h: int = h
        # Posición y velocidad de la cámara
        self.x: float = x

        # Interfaz
        self.interfaz: Interfaz = Interfaz(0, 500, 0, 3 - intentos)
        # Lista de enemigos, bloques y objetos
        self.enemigos: list = []
        self.bloques: list = []
        self.objetos: list = []
        # Lista de bloues, en el módulo de constantes están los datos para inicializar
        for _ in constantes.POSICION_BLOQUES:
            self.bloques.append(Bloque(*_))
        # Mario
        self.mario: Mario = Mario(*constantes.POSICION_INICIAL_M)
        # Atributo que comprueba si mario ha llegado al final
        self.final = False

    # MÉTODOS DE MOVIMIENTO
    def move(self):
        """movimiento de la camara. Si mario llega al límite de la pantalla se queda inmovil y se mueve el mapa con
        la misma velocidad"""
        # Límite del mapa
        if self.x > -1792:
            # Scroll junto con todos los elementos dibujados en él
            moverpx = 0
            if self.mario.position[0] > 112:
                self.mario.position[0] = 112
                moverpx = self.mario.velocidad[0]
            self.x -= moverpx
            # Si se mueve el escenario también se mueven los bloques y enemigos
            for bloque in self.bloques:
                bloque.move(moverpx)
            for enemigo in self.enemigos:
                enemigo.move(moverpx)
            for objeto in self.objetos:
                objeto.move(moverpx)
        # La cámara deja de moverse
        else:
            self.x = -1792

    # MÉTODOS DE CONTROL
    def finalNivel(self):
        """Función que comprueba si se ha llegado al final del nivel"""
        # si llega al final del mapa
        if self.x == -1792 and self.mario.position[0] > 128:
            # borramos la lista de enemgios
            self.enemigos.clear()
            # cambia el atributo del final
            self.final = True

    def inputs(self):
        """Recoge los distintas entradas del jugador"""
        # __direccion = 0
        self.mario.direccion_reset()
        # Input para __correr
        if pyxel.btn(pyxel.KEY_X):
            self.mario.sprint()
        else:
            self.mario.notsprint()
        # Izquierda
        if pyxel.btn(pyxel.KEY_LEFT):
            self.mario.direccion_left()
        # Derecha
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.mario.direccion_right()
        # Salto
        if pyxel.btn(pyxel.KEY_Z):
            self.mario.salto()
        # empezar de nuevo
        if pyxel.btnp(pyxel.KEY_R):
            self.__init__(constantes.WIDTH, constantes.HEIGHT, constantes.X, 0)

    def reiniciar(self):
        """Reinicio del nivel"""
        self.__init__(constantes.WIDTH, constantes.HEIGHT, constantes.X, self.intentos + 1)

    # SPAWN ENEMIGOS Y ELIMINACIÓN DE ELEMENTOS AL SALIR DE ESCENA
    def generarEnemigo(self):
        """Función encargada de generar enemigos con un límite de 4 a la vez en la pantalla. Los enemigos se generan
        en un momento aleatorio"""
        # momento aleatorio
        i = randint(1, 192)
        if pyxel.frame_count % i == 0:
            # Genera un enemigo (25% koopa 75% goomba)
            a = random()
            b = constantes.SPRITE_GOOMBA
            if a <= 0.25:
                b = constantes.SPRITE_KOOPA
            # Genera una y y una x random
            y = 208
            x = 256 + 16 * randint(0, 4)
            # Comprobamos que el enemigo no esté dentro de un bloque
            for bloque in self.bloques:
                while abs(bloque.x - x) <= 16 and -16 <= bloque.y - y < b[-1]:
                    x += 16
            # Si hay menos de 4 enemigos en pantalla
            if len(self.enemigos) < 4:
                # Generamos el enemigo si no está superpuesto con otro enemigo
                control = True
                for enemigo in self.enemigos:
                    if abs(enemigo.position[0] - x) <= 32:
                        control = False
                if control:
                    # Añadir enemigo a la lista con posición fuera de los límites de la cámara hacia la derecha
                    self.enemigos.append(Enemigo(x, y, 200, b))

    def borrarEnemigo(self):
        """Función encargada de eliminar un enemigo si este se sale por la izquierda o cae a un barranco"""
        # Bucle que recorre la lista de enemigos
        for enemigo in self.enemigos:
            if enemigo.position[0] < -16 or enemigo.position[1] >= 256:
                self.enemigos.remove(enemigo)

    def borrarObjeto(self):
        """Función encargada de eliminar un objeto si cae por un barranco"""
        # Bucle que recorre la lista de objetos
        for objeto in self.objetos:
            if objeto.position[1] >= 256:
                self.objetos.remove(objeto)

    def borrarBloque(self, bloque):
        """Función encargada de borrar bloques que se salen por la izquierda
        @param bloque: bloque que se evalúa si ha de ser borrado
        """
        if bloque.x < - 16:
            self.bloques.remove(bloque)

    # INTERACCIONES CON MARIO
    def interaccionMarioBloque(self, bloque):
        """Función que aplica la transformación adecuada a un bloque según su interación con mario
        @param bloque: bloque con el que se estña evaluando la interacción
        """
        # Si el bloque es un ladrillo y Mario es Super Mario
        if bloque.sprite == constantes.SPRITE_BLOQUE and self.mario.estado >= 1:
            self.bloques.remove(bloque)
        # Si el bloque es una interrogación o el bloque invisible
        if bloque.sprite == constantes.SPRITE_INTERR or bloque.sprite == constantes.INVISIBLE:
            # Si el bloque es invisible
            if bloque.sprite == constantes.INVISIBLE:
                # Se añade a la lista de objetos un 1-Up
                self.objetos.append(Objeto(bloque.x, bloque.y - 16, constantes.SPRITE_1UP, bloque.y - 16))
            # Si el bloque es una interrogación
            else:
                # Se crea una variable "posibilidad" que determina si el bloque contiene un champiñon o una moneda
                posibilidad = random()
                if posibilidad > 0.5:
                    # Se añade el objeto champiñon
                    self.objetos.append(Objeto(bloque.x, bloque.y - 16, constantes.SPRITE_CHAMPINON, bloque.y - 16))
                else:
                    # Se añade el objeto moneda
                    self.objetos.append(Objeto(bloque.x, bloque.y - 16, constantes.SPRITE_MONEDA, bloque.y - 16))
            # Se cambia el sprite por el de un bloque liso
            bloque.cambioBloqueLiso()

    def interaccionMarioEnemigo(self, enemigo, colision):
        """Función que evalúa la interaccíon de mario con un enemigo según su colisión
        @param enemigo: enemigo con el que se evalúa la interacción
        @param colision: lista de 2 booleanos, el primero indica si se ha colisionado y el segundo si ha sido desde
        arriba
        """
        # Si Mario colisiona con el enemigo
        if colision[0]:
            # Si Mario está arriba del enemigo
            if colision[1]:
                # Elimina el enemigo y suma puntuación. Luego hace que mario rebote
                self.enemigos.remove(enemigo)
                self.interfaz.sumarPuntuacion(200)
                self.mario.rebote()
            # Si Mario está debajo del enemigo
            else:
                # Mario toma daño
                self.mario.danno()

    def interaccionMarioObjeto(self, objeto, colision):
        """Función que evalúa la interaccíon de mario con un objeto según su colisión
                @param objeto: objeto con el que se evalúa la interacción
                @param colision: lista de booleanos que evalúa el choque
                """
        # Si mario choca con el objeto
        if colision[0]:
            # Si mario está en su estado original y el objeto con el que colisiona es un super champiñon
            if objeto.sprite == constantes.SPRITE_CHAMPINON and self.mario.estado < 1:
                self.mario.dannont()
            # Si objeto con el que colisiona es un 1-up
            elif objeto.sprite == constantes.SPRITE_1UP:
                self.interfaz.sumaVida()
                self.intentos -= 1
            # Si con el que colisiona es una moneda
            elif objeto.sprite == constantes.SPRITE_MONEDA:
                self.interfaz.sumarMonedas()
                self.interfaz.sumarPuntuacion(200)
            # Si mario es Super Mario y el objeto con el que colisiona es un super champiñon
            else:
                self.interfaz.sumarPuntuacion(1000)
            # Borra el objeto
            self.objetos.remove(objeto)

    # GENERAL
    def update(self):
        if not self.final and not self.interfaz.sinVidas:
            self.finalNivel()
            """Ejecuta todos los métodos en el orden correcto"""
            # Interfaz (tiempo, monedas, vidas...)
            self.interfaz.update()
            # Reinicia el nivel si mario muere o si se acaba el tiempo. También se reinicia si mario se cae
            if self.mario.estado <= -1 or self.interfaz.final_timer or self.mario.position[1] >= 255:
                self.reiniciar()
            # Generar enemigos
            self.generarEnemigo()
            # == Bucles de bloques y enemigos ==
            for bloque in self.bloques:
                # Colisión mario-bloque
                if self.mario.colisionBloque(bloque.colision2(self.mario)):
                    self.interaccionMarioBloque(bloque)
                # Si el bloque se sale de escena se borra
                self.borrarBloque(bloque)
                # Interacción con enemigos
                for enemigo in self.enemigos:
                    # colisión enemigo-bloque
                    enemigo.colisionBloque(bloque.colision2(enemigo))
                # Interaacción con objetos
                for objeto in self.objetos:
                    # colisión objeto-bloque
                    objeto.colisionBloque(bloque.colision2(objeto))
                    self.borrarObjeto()
            # Update de enemigo (debe ir en un bucle separado porque el anterior hizo todos los cálculos necesarios
            # para el enemigo: colisiones, __suelo. Esta función ahora se encarga de trabajar con esos datos)
            for enemigo in self.enemigos:
                enemigo.update()
                self.interaccionMarioEnemigo(enemigo, self.mario.colisionEntidad(enemigo))
            for objeto in self.objetos:
                objeto.update()
                self.interaccionMarioObjeto(objeto, self.mario.colisionEntidad(objeto))
            # Tras haber hecho las operaciones correspondientes con cada enemigo comprueba si se puede borrar y lo borra
            self.borrarEnemigo()
            # Update estado de mario
            self.mario.update()
            # Scroll (movimiento del mapa y lo que está dibujado encima)
            self.move()

    def draw(self):
        """Función encargada de dibujar el mapa y lo demás encima"""
        if not self.final:
            # Fondo
            pyxel.bltm(self.x, 0, 0, 0, 32, 256, 256)
            # Interfaz
            self.interfaz.draw()
            # Mario
            self.mario.draw()
            # Enemigos
            for enemigo in self.enemigos:
                enemigo.draw()
            # Bloques
            for bloque in self.bloques:
                bloque.draw()
            # Objetos
            for objeto in self.objetos:
                objeto.draw()
        elif self.final and self.interfaz.valores[3] > 0:
            pyxel.cls(0)
            pyxel.text(80, 123,
                       "HAS GANADO, ENHORABUENA.\n\nPulsa la tecla R para comenzar de nuevo\n\n Score: " + str(
                           self.interfaz.valores[0]) + "\n\nPulsa la Q para salir", 7)
        if self.interfaz.sinVidas:
            pyxel.cls(0)
            pyxel.text(80, 123, "GAME OVER\n\n Pulsa la tecla R para comenzar de nuevo.\n\nPulsa la Q para salir", 7)
