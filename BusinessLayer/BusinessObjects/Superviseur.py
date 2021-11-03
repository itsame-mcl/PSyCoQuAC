from BusinessLayer.BusinessObjects.agent import Agent

class Superviseur(Agent):

    def __init__(self, agent_id, nom_utilisateur, identite):
        super().__init__(agent_id, nom_utilisateur, identite)