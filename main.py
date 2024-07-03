# Rafael Bastos - 2110857
# Marcello Nascif -
# Thomas de Oliva -
import numpy as np
import pygame
from time import sleep

from view import Desenho
from particula import Particula
from barra import Barra
from corda import Corda


def distanciaParticulas(p1, p2):
    dist = (
        (p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1])
    ) ** 0.5

    return dist


def criaBarras(barras, particulas):
    ind = 0
    qtdPontos = len(particulas)

    while ind + 1 < qtdPontos:
        limite = min(qtdPontos, 8 + ind)

        p1 = particulas[ind]
        p2 = particulas[ind + 1]

        novaBarra = Barra(p1, p2, distanciaParticulas(p1.posicao, p2.posicao))

        barras = [novaBarra] + barras

        for i in range(ind + 2, limite):
            p3 = particulas[i]

            novaBarra = Barra(p1, p3, distanciaParticulas(p1.posicao, p3.posicao))

            barras.append(novaBarra)

        ind = ind + 1

    return barras


def relaxacao(barra):
    p1 = barra.p1
    p2 = barra.p2
    dist = distanciaParticulas(p1.posicao, p2.posicao)
    direcao = (p1.posicao - p2.posicao) / dist
    correcao = barra.tam - dist

    if not p1.mobilidade and not p2.mobilidade:
        p1.posicao = p1.posicao + direcao * (correcao / 2)
        p2.posicao = p2.posicao - direcao * (correcao / 2)

    elif not p1.mobilidade:
        p1.posicao = p1.posicao + direcao * correcao

    elif not p2.mobilidade:
        p2.posicao = p2.posicao - direcao * correcao


def inicializarCorda(dist, tam, passo, massa):
    pontos = []
    barras = []

    razaoDistCord = int(tam / dist)
    for i in range(razaoDistCord):
        posicaoAnt = np.array([dist * i, 11 + tam - dist * i])
        if i == 0:
            pontos.append(Particula( massa[i], posicaoAnt, True))
        else:
            pontos.append(Particula(massa[i], posicaoAnt, False))
            
    barras = criaBarras(barras, pontos)
    qtdParticulas = len(pontos)

    for i in range(qtdParticulas - 1):
        if not pontos[i].mobilidade:
            posicao = pontos[i].posicaoAnt + passo
            pontos[i].posicao = posicao

    posicao = pontos[-1].posicaoAnt + passo

    pontos[-1].posicao = posicao

    qtdBarras = len(barras)

    for i in range(qtdBarras - 1):
        relaxacao(barras[i])

    return barras, pontos


def passos(corda):
    delta = 0.02
    forcaG = np.array([0, -10])
    h = 1 / 60

    count = 0

    for p in corda.particulas:
        if p.mobilidade:
            continue

        posicaoAnt = p.posicaoAnt
        posicaoProx = p.posicao + (1 - delta) * (p.posicao - posicaoAnt) + ((h * h) / p.massa) * forcaG

        p.posicaoAnt = p.posicao
        p.posicao = posicaoProx

    for barra in corda.barras:
        relaxacao(barra)
        count = count + 1
    
    print("Iterações: ", count)
    return count


def Simulacao(view, corda):
    iteracoes = passos(corda)

    view.atualizaDesenho(corda.particulas)

    return iteracoes

distancia = 0.1
tamanho = 6
passo = 0.001
massa = [0.1 for i in range(60)]

view = Desenho()
corda = Corda(inicializarCorda(distancia, tamanho, passo, massa))

total_iteracoes = 0

while view.rodando():
    total_iteracoes += Simulacao(view, corda)

    view.clock.tick(60)

print("Total de iterações: ", total_iteracoes)
pygame.quit()
