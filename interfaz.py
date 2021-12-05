import pyxel
class Interfaz:
    """Función de la interfaz textual. Se inicializa(init) todo el rato para actualizar valores y se escribe"""
    def __init__(self, score, time, monedas, nivel, mundo, vidas):
        self.valores = [score, time, monedas, nivel, mundo, vidas]
        self.final_timer: bool = False

    def timer(self):
        if self.valores[1] > 0:
            if pyxel.frame_count % 30 == 0:
                self.valores[1] -= 1
        if self.valores[1] == 0:
            self.final_timer = True

    def update(self):
        self.timer()

    def draw(self):
        pyxel.text(5,5,"SCORE: %i" %self.valores[0], 7)
        pyxel.blt(84, 2 , 0, 51, 34, 10, 12)
        pyxel.text(100, 5, "x %i" %self.valores[2], 7)
        pyxel.text(220, 5, "TIME: %i" %self.valores[1], 7)
