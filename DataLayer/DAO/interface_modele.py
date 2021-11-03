from abc import ABC, abstractmethod

class InterfaceModele(ABC):

    @abstractmethod
    def recuperer_modele(self, identifiant: int) -> dict:
        raise NotImplementedError

    def recuperer_regex(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def creer_modele(self, data: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def modifier_modele(self, data: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def supprimer_modele(self, identifiant: int) -> bool:
        raise NotImplementedError
