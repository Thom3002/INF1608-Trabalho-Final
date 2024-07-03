class Particula:
    def __init__(self, massa, posicao, imovel):
        self._massa = massa
        self._posicaoAnt = posicao
        self._posicao = posicao
        self._imovel = imovel

    @property
    def massa(self):
        return self._massa

    @property
    def posicaoAnt(self):
        return self._posicaoAnt

    @property
    def posicao(self):
        return self._posicao

    @property
    def mobilidade(self):
        return self._imovel

    @posicao.setter
    def posicao(self, posicao):
        self._posicao = posicao

    @posicaoAnt.setter
    def posicaoAnt(self, posicao):
        self._posicaoAnt = posicao
        