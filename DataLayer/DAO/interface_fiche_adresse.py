from abc import ABC, abstractmethod
from typing import List


class InterfaceFicheAdresse(ABC):

    @abstractmethod
    def recuperer_fiche_adresse(self, identifiant: int) -> dict:
        raise NotImplementedError

    @abstractmethod
    def recuperer_liste_fiches_adresse(self, id_agent: int, id_lot: int) -> List[dict]:
        raise NotImplementedError

    @abstractmethod
    def creer_fiche_adresse(self, data: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def modifier_fiche_adresse(self, data: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def modifier_agent_fiches_adresse(self, id_agent : int, id_fas : List[int]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def supprimer_fiche_adresse(self, identifiant: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def obtenir_statistiques(self, champs: list) -> List[tuple]:
        raise NotImplementedError

    @abstractmethod
    def recuperer_dernier_id_fa(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def recuperer_dernier_id_lot(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def incrementer_id_lot(self) -> bool:
        raise NotImplementedError
