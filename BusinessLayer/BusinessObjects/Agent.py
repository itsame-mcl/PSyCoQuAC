class Agent:

    def __init__(self, agent_id, nom_utilisateur, identite):
        self._agent_id = agent_id
        self._nom_utilisateur = nom_utilisateur
        self._identite = identite
    
    @property
    def agent_id(self):
        return self._agent_id
    
    @property
    def nom_utilisateur(self):
        return self._nom_utilisateur

    @property
    def identite(self):
        return self._identite
    
    @identite.setter
    def agent_id(self, value): # le setter prend un argument un Tuple. Possibilité qu'il prenne 2 String (nom & prénom)
        self._agent_id = value