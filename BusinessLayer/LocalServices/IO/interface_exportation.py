from abc import ABC, abstractmethod

class InterfaceExportation(ABC):

    @abstractmethod
    def exporter_lot(self, fichier):
        raise NotImplemented