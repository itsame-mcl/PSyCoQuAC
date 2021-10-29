class Session:

    def __init__(self, utilisateur_connecte, droits_utilisateurs):
        self._utilisateur_connecte = utilisateur_connecte
        self._droits_utilisateurs = droits_utilisateurs

    @property
    def utilisateur_connecte(self):
        return self._utilisateur_connecte # ce getter renvoie un Agent
    
    @property
    def droits_utilisateurs(self):
        return self._droits_utilisateurs