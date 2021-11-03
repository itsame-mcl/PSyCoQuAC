from BusinessLayer.BusinessObjects.agent import Agent

class Session:

    def __init__(self, utilisateur_connecte : Agent, droits_superviseurs):
        self._utilisateur_connecte = utilisateur_connecte
        self._droits_superviseurs = droits_superviseurs

    @property
    def utilisateur_connecte(self) -> Agent:
        return self._utilisateur_connecte
    
    @property
    def droits_superviseurs(self):
        return self._droits_superviseurs