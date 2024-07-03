import pygame
from time import perf_counter

comprimento = 600
altura = 400


class Desenho:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((comprimento, altura))
        pygame.display.set_caption("Corda: ")
        self.clock = pygame.time.Clock()
        self.tempo = 0
        self.tam = 15
        self.conversor = self.coordenadas(self.tam)
        self.running = True

    def coordenadas(self, tam):
        def interno(c):
            valor1 = comprimento / 2.0 * (1 + c.posicao[0] / tam)
            valor2 = altura * (1 - 0.8 * c.posicao[1] / tam)
            return valor1, valor2

        return interno

    def atualizaDesenho(self, pontos):
        self.screen.fill((255, 255, 255))

        pontos_abs = list(map(self.conversor, pontos))
        if len(pontos_abs) > 1:
            pygame.draw.lines(self.screen, (255, 0, 0), False, pontos_abs, 2)

        pygame.display.flip()

        while perf_counter() - self.tempo < 1 / 48:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

        self.tempo = perf_counter()

    def rodando(self):
        return self.running
