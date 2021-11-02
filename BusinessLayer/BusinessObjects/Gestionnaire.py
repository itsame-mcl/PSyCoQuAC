from BusinessLayer.BusinessObjects.agent import Agent

class Gestionnaire(Agent):

    def __init__(self, agent_id, nom_utilisateur, identite, superviseur_id):
        super().__init__(agent_id, nom_utilisateur, identite)
        self._superviseur_id = superviseur_id

    @property
    def superviseur_id(self):
        return self._superviseur_id