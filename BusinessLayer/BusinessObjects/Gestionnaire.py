from BusinessLayer.BusinessObjects.agent import Agent
from typing import Tuple

class Gestionnaire(Agent):

    def __init__(self, agent_id : int, nom_utilisateur : str, identite : Tuple, superviseur_id : int):
        super().__init__(agent_id, nom_utilisateur, identite)
        self._superviseur_id = superviseur_id

    @property
    def superviseur_id(self) -> int:
        return self._superviseur_id