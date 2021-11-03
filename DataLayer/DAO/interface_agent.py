from typing import Tuple
from typing import List
from abc import ABC, abstractmethod
from BusinessLayer.BusinessObjects.agent import Agent

class InterfaceAgent(ABC):

    def deleguer_agent_a(self, id_agents : List[int], id_superviseur : int) -> bool:
        raise NotImplementedError

    def recuperer_liste_agents(self, id_superviseur : int) -> List[Agent]:
        raise NotImplementedError

    def supprimer_agent(self, id_agent : int) -> bool:
        raise NotImplementedError

    def creer_agent(self,  est_superviseur : bool, quotite : float, id_superviseur : int, nom_utilisateur : str, mot_de_passe : str, prenom : str, nom : str) -> bool:
        raise NotImplementedError

    def modifier_agent(self, agent_a_modifier : Agent) -> bool:
        raise NotImplementedError

    def changer_droits(self, agent_a_modifier : Agent) -> bool:
        raise NotImplementedError

    def recuperer_mdp_agent(self, nom_utilisateur : str, mot_de_passe : str) -> str:
        raise NotImplementedError
    
    def recuperer_agent_id(self, nom_utilisateur : str, mot_de_passe : str) -> int:
        raise NotImplementedError

    def recuperer_agent_identite(self, nom_utilisateur : str, mot_de_passe : str) -> Tuple:
        raise NotImplementedError

    def recuperer_superviseur_id(self, nom_utilisateur : str, mot_de_passe : str) -> int:
        raise NotImplementedError