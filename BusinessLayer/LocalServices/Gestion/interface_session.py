from abc import ABC, abstractmethod

class InterfaceSession(ABC):

    @abstractmethod
    def ouvrir_session(self, nom_utilisateur, mot_de_passe):
        raise NotImplemented

    @abstractmethod
    def fermer_session(self):
        raise NotImplemented