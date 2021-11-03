from BusinessLayer.BusinessObjects.agent import Agent
from typing import Tuple

class Superviseur(Agent):

    def __init__(self, agent_id : int, nom_utilisateur : str, identite : Tuple):
        super().__init__(agent_id, nom_utilisateur, identite)