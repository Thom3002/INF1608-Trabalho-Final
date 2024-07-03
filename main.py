# Rafael Bastos - 2110857
# Marcello Nascif -
# Thomas de Oliva -
import numpy as np
from view import Desenho

class Particula:
    def __init__(self, imovel, posicao, massa):
        self.massa = massa
        self.posicaoAnt = posicao
        self.posicao = posicao
        self.imovel = imovel

class Barra:
    def __init__(self, p1, p2):
        self.p1 = p1; self.p2 = p2
        self.tam = DistanciaParticulas(GetPosicao(p1), GetPosicao(p2))
        
class Corda:
    def __init__(self):
        self.barras, self.particulas = inicializarCorda([],[],0.1,6,0.001,[0.1 for i in range(60)])

def GetPosicao(particula):
    return particula.posicao

def AtualizaPosicao(particula, posicaoProx):
    particula.posicaoAnt = particula.posicao
    particula.posicao = posicaoProx
    
def DistanciaParticulas(p1, p2):
    dist = ((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1])) ** 0.5
    return dist

def GetMobilidade(particula):
    return particula.imovel

def Relaxacao(barra):
    p1 = barra.p1; p2 = barra.p2
    dist = DistanciaParticulas(GetPosicao(p1), GetPosicao(p2))
    direcao = (GetPosicao(p1) - GetPosicao(p2))/dist
    correcao = barra.tam - dist
    if not GetMobilidade(p1) and not GetMobilidade(p2):
        p1.posicao = p1.posicao + direcao*(correcao/2)
        p2.posicao = p2.posicao - direcao*(correcao/2)
    elif not GetMobilidade(p1):
        p1.posicao = p1.posicao + direcao*correcao
    elif not GetMobilidade(p2):
        p2.posicao = p2.posicao - direcao*correcao

def CriaBarras(barras, particulas):
    ind = 0
    qtdPontos = len(particulas)
    while (ind + 1 < qtdPontos):
        limite = min(qtdPontos, 8+ind) 
        p1 = particulas[ind]; p2 = particulas[ind + 1]
        novaBarra = Barra(p1,p2)
        barras = [novaBarra] + barras

        for i in range(ind + 2, limite):
            p3 = particulas[i]
            novaBarra = Barra(p1,p3)
            barras.append(novaBarra)
        
        ind = ind + 1

    return barras

def inicializarCorda(pontos, barras, dist, tam, passo, massa):
    razaoDistCord = int(tam / dist)
    for i in range(razaoDistCord):
        posicaoAnt = np.array([dist * i, 11 + tam - dist * i])
        if i == 0:
            pontos.append(Particula(True, posicaoAnt, massa[i]))
        else:
            pontos.append(Particula(False, posicaoAnt, massa[i]))
    barras = CriaBarras(barras,pontos)
    qtdParticulas = len(pontos)
    for i in range(qtdParticulas - 1):
        if not GetMobilidade(pontos[i]):
            posicao = pontos[i].posicaoAnt + passo
            AtualizaPosicao(pontos[i],posicao)
    posicao = pontos[-1].posicaoAnt + passo
    AtualizaPosicao(pontos[-1],posicao)
    qtdBarras = len(barras)
    for i in range(qtdBarras - 1):
        Relaxacao(barras[i])

    return barras, pontos

def passos(corda):
    delta = 0.02
    count = 0
    forcaG = np.array([0, -10]) #Atua apenas no eixo Y
    h = 1/60
    for i, p in enumerate(corda.particulas):
        if GetMobilidade(p):
            continue
        # Integracao de Verlet
        posicaoAnt = p.posicaoAnt
        PosicaoProx = p.posicao + (1 - delta) * (p.posicao - posicaoAnt) + ((h*h) / p.massa) * forcaG

        AtualizaPosicao(p,PosicaoProx)
    for i in range(len(corda.barras)):
        Relaxacao(corda.barras[i])
        count += 1

    return

def GetParticulas(corda,pontos):
    for ponto in corda.particulas:
        posicao = GetPosicao(ponto).tolist()
        pontos.append(posicao)
    return pontos

def Simulacao(view,corda):
    passos(corda)
    view.atualizaDesenho(GetParticulas(corda,[]))


view = Desenho()
corda = Corda()

while (view):
    Simulacao(view,corda)