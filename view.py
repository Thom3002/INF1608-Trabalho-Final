import tkinter as tk
from time import perf_counter

comprimento = 600
altura = 400

class Desenho:
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=comprimento, height=altura)
        self.canvas.pack()
        self.tempo = 0
        self.tam = 15
        self.conversor = self.coordenadas(self.tam)

        self.root.title("Corda: ")
        self.root.protocol("WM_DELETE_WINDOW", self._fechar)

    def _fechar(self):
        self.root.destroy()

    def coordenadas(self,tam):
        def interno(c):
            valor1 = comprimento / 2.0 * (1 + c[0] / tam)
            valor2 = altura * (1 - 0.8 * c[1] / tam)
            return valor1, valor2
        return interno

    def atualizaDesenho(self, pontos):
        self.canvas.delete(tk.ALL)

        pontos_abs = list(map(self.conversor, pontos))
        self.canvas.create_line(pontos_abs, fill='red')

        self.root.update()

        while perf_counter() - self.tempo < 1 / 48:
            self.root.update()

        self.tempo = perf_counter()

