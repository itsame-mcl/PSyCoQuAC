class Adresse:
    def __init__(self, numero, voie, cp, ville):
        self._numero = numero
        self._voie = voie
        self._cp = cp
        self._ville = ville

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, value):
        self._numero = value

    @property
    def voie(self):
        return self._voie

    @voie.setter
    def voie(self, value):
        self._voie = value

    @property
    def cp(self):
        return self._cp

    @cp.setter
    def cp(self, value):
        self._cp = value

    @property
    def ville(self):
        return self._ville

    @ville.setter
    def ville(self, value):
        self._ville = value
