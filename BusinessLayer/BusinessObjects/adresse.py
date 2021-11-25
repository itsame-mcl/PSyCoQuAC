class Adresse:
    def __init__(self, numero, voie, cp, ville):
        """

        :param numero:
        le numéro de l'adresse
        :param voie:
        le type de voie (rue, impasse, avenue, boulevard) de l'adresse
        :param cp:
        le code postal de l'adresse
        :param ville:
        le nom de la ville de l'adresse
        """
        self._numero = str(numero)
        self._voie = str(voie)
        self._cp = str(cp)
        self._ville = str(ville)

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, value):
        self._numero = str(value)

    @property
    def voie(self):
        return self._voie

    @voie.setter
    def voie(self, value):
        self._voie = str(value)

    @property
    def cp(self):
        return self._cp

    @cp.setter
    def cp(self, value):
        self._cp = str(value)

    @property
    def ville(self):
        return self._ville

    @ville.setter
    def ville(self, value):
        self._ville = str(value)

    def __str__(self):
        res = str(self.numero) + " " + str(self.voie) + " " + str(self.cp) + " " + str(self.ville)
        return res

    def __eq__(self, other):
        res = self.numero == other.numero
        res *= self.voie == other.voie
        res *= self.cp == other.cp
        res *= self.ville == other.ville
        return res
