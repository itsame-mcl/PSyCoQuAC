from typing import List
from abc import ABC, abstractmethod
from BusinessLayer.BusinessObjects.agent import Agent


class InterfaceAgent(ABC):
    @abstractmethod
    def deleguer_agent_a(self, id_agents : List[int], id_superviseur : int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def recuperer_agent(self, id_agent: int) -> dict:
        raise NotImplementedError

    @abstractmethod
    def recuperer_equipe(self, id_superviseur : int) -> List[dict]:
        raise NotImplementedError

    @abstractmethod
    def supprimer_agent(self, id_agent : int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def creer_agent(self, data: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def modifier_agent(self, data: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def changer_droits(self, agent_a_modifier : Agent) -> bool:
        raise NotImplementedError
