from typing import Tuple

class Agent:

    def __init__(self, agent_id : int, nom_utilisateur : str, identite : Tuple, quotite: float):
        self._agent_id = agent_id
        self._nom_utilisateur = nom_utilisateur
        self._identite = identite
        self._quotite = quotite
    
    @property
    def agent_id(self) -> int:
        return self._agent_id
    
    @property
    def nom_utilisateur(self) -> str:
        return self._nom_utilisateur

    @property
    def identite(self) -> Tuple:
        return self._identite
    
    @identite.setter
    def identite(self, value : Tuple): # le setter prend un argument un Tuple. Possibilité qu'il prenne 2 String (nom & prénom)
        self._identite = value

    @property
    def quotite(self) -> float:
        return self._quotite
    
    @quotite.setter
    def quotite(self, value):
        self._quotite = value

