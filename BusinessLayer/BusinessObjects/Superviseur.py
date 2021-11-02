from BusinessLayer.BusinessObjects.Agent import Agent

class Gestionnaire(Agent):

    def __init__(self, agent_id, nom_utilisateur, identite, equipe_deleguee_a):
        super().__init__(agent_id, nom_utilisateur, identite)
        self._equipe_deleguee_a = equipe_deleguee_a

    @property
    def equipe_deleguee_a(self):
        return self._equipe_deleguee_a