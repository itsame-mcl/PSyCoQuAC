from abc import ABC, abstractmethod


class InterfaceConnexion(ABC):
    @abstractmethod
    def ouvrir_connexion(self, host, port, database, user, password):
        raise NotImplemented

    @abstractmethod
    def fermer_connexion(self, connexion):
        raise NotImplemented
