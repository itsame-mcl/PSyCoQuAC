from abc import ABC, abstractmethod


class InterfaceExportation(ABC):

    @abstractmethod
    def exporter_lot(self, id_lot, chemin_destination):
        raise NotImplemented
