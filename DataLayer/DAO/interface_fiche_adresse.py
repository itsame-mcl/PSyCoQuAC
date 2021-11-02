from abc import ABC, abstractmethod


class InterfaceFicheAdresse(ABC):
    @abstractmethod
    def recuperer_fiche_adresse(self, identifiant : int) -> dict:
        raise NotImplementedError

    def creer_fiche_adresse(self, data : dict) -> bool:
        raise NotImplementedError

    def modifier_fiche_adresse(self, data : dict) -> bool:
        raise NotImplementedError

    def supprimer_fiche_adresse(self, identifiant : int) -> bool:
        raise NotImplementedError
