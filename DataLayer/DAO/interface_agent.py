from abc import ABC, abstractmethod

from BusinessLayer.BusinessObjects.Agent import Agent


class InterfaceAgent(ABC):

    @abstractmethod # methode realisable seulement par un superviseur
    def deleguer_agent_a(self, id_agents : List[int], id_superviseur_actuel : int, id_superviseur_futur : int):
        raise NotImplemented

    @abstractmethod
    def recuperer_fiches_agent(self, id_agent : int) -> List[dict]:
        raise NotImplemented

    @abstractmethod
    def recuperer_liste_agents(self, id_superviseur : int) -> List[Agent]:
        raise NotImplemented

    @abstractmethod
    def supprimer_agent(self, id_agent : int) -> bool:
        raise NotImplemented
