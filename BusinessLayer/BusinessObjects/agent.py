from typing import Tuple

class Agent:

    def __init__(self, agent_id : int, prenom : str, nom : str, quotite: float):
        self._agent_id = agent_id
        self._prenom = prenom
        self._nom = nom
        self._quotite = quotite
    
    @property
    def agent_id(self) -> int:
        return self._agent_id
    
    @property
    def prenom(self) -> str:
        return self._nom_utilisateur
    
    @prenom.setter
    def prenom(self, value : str):
        self._prenom = value

    @property
    def nom(self) -> str:
        return self._identite
    
    @nom.setter
    def nom(self, value : str):
        self._nom = value

    @property
    def quotite(self) -> float:
        return self._quotite
    
    @quotite.setter
    def quotite(self, value):
        self._quotite = value