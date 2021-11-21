from typing import List
from abc import ABC, abstractmethod


class InterfaceAgent(ABC):
    @abstractmethod
    def recuperer_agent(self, id_agent: int) -> dict:
        raise NotImplementedError

    @abstractmethod
    def recuperer_liste_agents(self, id_superviseur: int, agents_delegues: bool = False) -> List[dict]:
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
    def deleguer_agent(self, id_agent: int, id_superviseur_delegue: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def retroceder_agent(self, id_agent: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def transferer_agent(self, id_agent: int, id_nouveau_superviseur: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def promouvoir_agent(self, agent_a_promouvoir: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def modifier_identifiants(self, id_agent: int, nom_utilisateur: str, mdp_sale_hashe: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def verifier_identifiants(self, id_agent: int, nom_utilisateur: str, mdp_sale_hashe: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def connexion_agent(self, nom_utilisateur: str, mdp_sale_hashe: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    def recuperer_quotite(self, id_agent: int) -> float:
        raise NotImplementedError

    @abstractmethod
    def recuperer_nom_utilisateur(self, id_agent: int) -> str:
        raise NotImplementedError

    @abstractmethod
    def recuperer_dernier_id_agent(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def recuperer_id_superviseur(self, id_agent: int) -> int:
        raise NotImplementedError
