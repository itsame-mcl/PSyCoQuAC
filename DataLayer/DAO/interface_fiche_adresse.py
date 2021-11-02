from abc import ABC, abstractmethod


class InterfaceFicheAdresse(ABC):
    @abstractmethod
    def recuperer_fiche_adresse(self, identifiant):
        raise NotImplementedError
