from abc import ABC, abstractmethod

class InterfaceExportation(ABC):

    @abstractmethod
    def exporattion(self, fichier):
        raise NotImplemented