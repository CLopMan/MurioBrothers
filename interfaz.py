import pyxel
import constantes

class Interfaz:
    """interfaz con texto. Información al usuario y guarda datos relevantes"""
    def __init__(self, score: int, time: int, monedas: int, vidas: int):
        """Inicialización de la interfaz
        @param score: puntuacíon de mario
        @param time: tiempo restante para superar el nivel
        @param monedas: monedas recogidas
        @param vidas: vidas restantes de mario
        """
        self.valores: list = [score, time, monedas, vidas]
        self.final_timer = False

    # Atributos de sólo lectura
    @property
    def sinVidas(self):
        """Bool que indica si Mario no tiene más vidas"""
        if self.valores[3] == 0:
            return True
        else:
            return False

    # TEMPORIZADOR
    def timer(self):
        """Contador del tiempo"""
        # Si el tiempo es mayor a 0 resta 1 por cada 30 frames (1 s)
        if self.valores[1] > 0:
            if pyxel.frame_count % 30 == 0:
                self.valores[1] -= 1
        # Si el tiempo se acaba devuelve un True
        if self.valores[1] == 0:
            return True
        else:
            return False

    # VIDAS
    def restarVidas(self):
        """Resta una vida a mario"""
        self.valores[3] -= 1

    # BENEFICIOES
    def sumaVida(self):
        """Suma una vida a mario"""
        self.valores[3] += 1

    def sumarPuntuacion(self, valor: int):
        """Suma x puntos al marcador de Mario
        @param valor: puntación que hay que sumar
        """
        self.valores[0] += valor

    def sumarMonedas(self):
        """Suma 1 al contador de monedas"""
        self.valores[2] += 1

    # GENERAL
    def update(self):
        """Update de la interfaz"""
        self.final_timer = self.timer()

    def draw(self):
        """Dibujo de la interfaz"""
        pyxel.text(5, 5, "SCORE: %i" %self.valores[0], 7)
        pyxel.blt(84, 5, *constantes.SPRITE_MONEDA)
        pyxel.text(100, 5, "x %i" %self.valores[2], 7)
        pyxel.blt(148, 2, *constantes.SPRITE_1UP, colkey=0)
        pyxel.text(164, 5, "x %i" %self.valores[3], 7)
        pyxel.text(220, 5, "TIME: %i" %self.valores[1], 7)

