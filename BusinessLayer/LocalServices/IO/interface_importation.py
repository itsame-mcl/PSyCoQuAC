from abc import ABC, abstractmethod

class InterfaceImportation(ABC):

    @abstractmethod
    def importer_lot(self, agent, id_lot, chemin_fichier):
        raise NotImplemented