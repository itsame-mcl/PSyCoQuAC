from abc import ABC, abstractmethod


class InterfaceFicheAdresse(ABC):
    @abstractmethod
    def recuperer_fiche_adresse(self, identifiant : int) -> dict:
        raise NotImplementedError

    def creer_fiche_adresse(self, dictionnaire : dict) -> bool:
        raise NotImplementedError
