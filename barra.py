class Barra:
    def __init__(self, p1, p2, tam):
        self._p1 = p1
        self._p2 = p2
        self.tam = tam

    @property
    def p1(self):
        return self._p1

    @property
    def p2(self):
        return self._p2
