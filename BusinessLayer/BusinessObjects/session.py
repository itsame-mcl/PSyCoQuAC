class Session:

    def __init__(self, utilisateur_connecte, droits_superviseurs):
        self._utilisateur_connecte = utilisateur_connecte
        self._droits_superviseurs = droits_superviseurs

    @property
    def utilisateur_connecte(self):
        return self._utilisateur_connecte # ce getter renvoie un Agent
    
    @property
    def droits_superviseurs(self):
        return self._droits_superviseurs