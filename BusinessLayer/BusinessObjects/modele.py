class Modele:

    def __init__(self, nom_modele, regex_nom_fichier, correspondances):
        self._nom_modele = nom_modele
        self._regex = regex_nom_fichier
        self._correspondances = correspondances
    
    @property
    def nom_modele(self):
        return self._nom_modele

    @nom_modele.setter
    def nom_modele(self, value):
        self._nom_modele = value

    @property
    def regex(self):
        return self._regex

    @regex.setter
    def regex(self, value):
        self._regex = value

    @property
    def correspondances(self):
        return self._correspondances

    @correspondances.setter
    def correspondances(self, value):
        self._correspondances = value

    def as_dict(self) -> bool:
        data = dict()
        data["nom_modele"] = self._nom_modele
        data["regex_nom_fichier"] = self._regex

