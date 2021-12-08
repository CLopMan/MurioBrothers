import pyxel
import constantes

class Interfaz:
    """interfaz con texto. Información al usuario y guarda datos relevantes"""
    def __init__(self, score, time, monedas, nivel, mundo, vidas):
        self.valores: list = [score, time, monedas, nivel, mundo, vidas]
        self.final_timer: bool = False

    def timer(self):
        """Contador del tiempo"""
        # Si el tiempo es mayor a 0 resta 1 por cada 30 frames (1 s)
        if self.valores[1] > 0:
            if pyxel.frame_count % 30 == 0:
                self.valores[1] -= 1
        if self.valores[1] == 0:
            self.final_timer = True

    def restarVidas(self):
        """Resta una vida a mario"""
        self.valores[5] -= 1

    def sumarPuntuacion(self, valor):
        """Suma x puntos al marcador de Mario"""
        self.valores[0] += valor

    def sumarMonedas(self):
        """Suma 1 al contador de monedas"""
        self.valores[2] += 1

    def update(self):
        """Update de la interfaz"""
        self.timer()

    def draw(self):
        """Dibujo de la interfaz"""
        pyxel.text(5, 5, "SCORE: %i" %self.valores[0], 7)
        pyxel.blt(84, 15, *constantes.SPRITE_MONEDA)
        pyxel.text(100, 5, "x %i" %self.valores[2], 7)
        pyxel.blt(148, 2, *constantes.SPRITE_1UP, colkey=0)
        pyxel.text(164, 5, "x %i" %self.valores[5], 7)
        pyxel.text(220, 5, "TIME: %i" %self.valores[1], 7)
