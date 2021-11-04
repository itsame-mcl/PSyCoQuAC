from typing import List
from abc import ABC, abstractmethod


class InterfaceAgent(ABC):
    @abstractmethod
    def recuperer_agent(self, id_agent: int) -> dict:
        raise NotImplementedError

    @abstractmethod
    def recuperer_liste_agents(self, id_superviseur: int) -> List[dict]:
        raise NotImplementedError

    @abstractmethod
    def supprimer_agent(self, id_agent: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def creer_agent(self, data: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def modifier_agent(self, data: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def modifier_superviseur(self, id_agents: List[int], id_superviseur: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def changer_droits(self, data: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def connexion_agent(self, nom_utilisateur: str, mdp_sale_hashe: str) -> dict:
        raise NotImplementedError
