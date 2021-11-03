from abc import ABC, abstractmethod
from BusinessLayer.BusinessObjects.agent import Agent

class InterfaceFicheAgent(ABC):

    @abstractmethod
    def creer_agent(self, est_superviseur : bool, quotite : float, id_superviseur : int, nom_utilisateur : str, mot_de_passe : str, prenom : str, nom : str):
        raise NotImplemented

    @abstractmethod
    def modifier_agent(self, agent_a_modifier : Agent, data : dict):
        raise NotImplemented

    @abstractmethod
    def changer_droits(self, agent_a_modifier: Agent):
        raise NotImplemented

    @abstractmethod
    def supprimer_agent(self, agent_a_supprimer : Agent):
        raise NotImplemented