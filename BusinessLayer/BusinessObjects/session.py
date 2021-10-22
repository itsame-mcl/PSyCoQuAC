from agent.py import Agent

class Session(Agent):

    def __init__(self, utilisateur_connecte, droits_utilisateurs):
        self._utilisateur_connecte = utilisateur_connecte
        self._droits_utilisateurs = droits_utilisateurs

    @property
    def utilisateur_connecte(self):
        return self._utilisateur_connecte
    
    @property
    def droits_utilisateurs(self):
        return self._droits_utilisateurs