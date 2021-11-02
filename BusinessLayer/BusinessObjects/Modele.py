class Modele:

    def __init__(self, nom_modele, regex_nom_fichier, correspondances):
        self._nom_modele = nom_modele
        self._regex_nom_fichier = regex_nom_fichier
        self._correspondances = correspondances
    
    @property
    def nom_modele(self):
        return self._nom_modele

    @property
    def regex_nom_fichier(self):
        return self._regex_nom_fichier

    @property
    def correspondances(self):
        return self._correspondances