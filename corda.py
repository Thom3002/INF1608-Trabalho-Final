class Corda:
    def __init__(self, particulas):
        self._barras, self._particulas = particulas

    @property
    def barras(self):
        return self._barras

    @property
    def particulas(self):
        return self._particulas
