from abc import ABC, abstractmethod
from typing import List


class InterfaceFicheAdresse(ABC):
    @abstractmethod
    def recuperer_fiche_adresse(self, identifiant: int) -> dict:
        raise NotImplementedError

    def recuperer_liste_fiches_adresse(self, id_agent: int, id_lot: int) -> List[dict]:
        raise NotImplementedError

    def creer_fiche_adresse(self, data: dict) -> bool:
        raise NotImplementedError

    def modifier_fiche_adresse(self, data: dict) -> bool:
        raise NotImplementedError

    def supprimer_fiche_adresse(self, identifiant: int) -> bool:
        raise NotImplementedError
