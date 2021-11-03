from abc import ABC, abstractmethod

class InterfaceModele(ABC):

    def creer_modele(self, data: dict) -> bool:
        raise NotImplementedError
