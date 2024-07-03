# Rafael Bastos - 2110857
# Marcello Nascif -
# Thomas de Oliva -
import numpy as np
from view import Desenho
from particula import Particula
from barra import Barra
from corda import Corda


def DistanciaParticulas(p1, p2):
    dist = (
        (p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1])
    ) ** 0.5

    return dist


def CriaBarras(barras, particulas):
    ind = 0
    qtdPontos = len(particulas)

    while ind + 1 < qtdPontos:
        limite = min(qtdPontos, 8 + ind)

        p1 = particulas[ind]
        p2 = particulas[ind + 1]

        novaBarra = Barra(p1, p2, DistanciaParticulas(p1.posicao, p2.posicao))

        barras = [novaBarra] + barras

        for i in range(ind + 2, limite):
            p3 = particulas[i]

            novaBarra = Barra(p1, p3, DistanciaParticulas(p1.posicao, p3.posicao))

            barras.append(novaBarra)

        ind = ind + 1

    return barras


def Relaxacao(barra):
    p1 = barra.p1
    p2 = barra.p2
    dist = DistanciaParticulas(p1.posicao, p2.posicao)
    direcao = (p1.posicao - p2.posicao) / dist
    correcao = barra.tam - dist

    if not p1.mobilidade and not p2.mobilidade:
        p1.posicao = p1.posicao + direcao * (correcao / 2)
        p2.posicao = p2.posicao - direcao * (correcao / 2)

    elif not p1.mobilidade:
        p1.posicao = p1.posicao + direcao * correcao

    elif not p2.mobilidade:
        p2.posicao = p2.posicao - direcao * correcao


def inicializarCorda(pontos, barras, dist, tam, passo, massa):
    razaoDistCord = int(tam / dist)
    for i in range(razaoDistCord):
        posicaoAnt = np.array([dist * i, 11 + tam - dist * i])
        if i == 0:
            pontos.append(Particula(True, posicaoAnt, massa[i]))
        else:
            pontos.append(Particula(False, posicaoAnt, massa[i]))
    barras = CriaBarras(barras, pontos)
    qtdParticulas = len(pontos)

    for i in range(qtdParticulas - 1):
        if not pontos[i].mobilidade:
            posicao = pontos[i].posicaoAnt + passo
            pontos[i].posicao = posicao

    posicao = pontos[-1].posicaoAnt + passo

    pontos[-1].posicao = posicao

    qtdBarras = len(barras)

    for i in range(qtdBarras - 1):
        Relaxacao(barras[i])

    return barras, pontos


def passos(corda):
    delta = 0.02
    count = 0
    forcaG = np.array([0, -10])  # Atua apenas no eixo Y
    h = 1 / 60
    for i, p in enumerate(corda.particulas):
        if p.mobilidade:
            continue
        # Integracao de Verlet
        posicaoAnt = p.posicaoAnt
        PosicaoProx = (
            p.posicao
            + (1 - delta) * (p.posicao - posicaoAnt)
            + ((h * h) / p.massa) * forcaG
        )

        p.posicao = PosicaoProx
    for i in range(len(corda.barras)):
        Relaxacao(corda.barras[i])
        count += 1

    return


def Simulacao(view, corda):
    passos(corda)

    lstAux = corda.particulas
    view.atualizaDesenho(lstAux)


view = Desenho()
corda = Corda(inicializarCorda([], [], 0.1, 6, 0.001, [0.1 for i in range(60)]))

while view:
    Simulacao(view, corda)
