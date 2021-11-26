import pyxel
class Interfaz:
    """Función de la interfaz textual. Se inicializa(init) todo el rato para actualizar valores y se escribe"""
    def __init__(self,score, time, monedas, nivel, mundo, vidas):
        self.valores = [score, time, monedas, nivel, mundo, vidas]
    def draw(self):
        pyxel.text(5,5,"%i" %self.valores[0], 7)
        pyxel.text(240, 5, "%i" %self.valores[1], 7)
