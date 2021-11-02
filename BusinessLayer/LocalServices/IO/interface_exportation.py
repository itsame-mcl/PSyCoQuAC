from abc import ABC, abstractmethod

class InterfaceExportation(ABC):

    @abstractmethod
    def exportation(self, fichier):
        raise NotImplemented