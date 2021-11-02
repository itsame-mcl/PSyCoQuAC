from abc import ABC, abstractmethod

class InterfaceFicheAgent(ABC):

    @abstractmethod
    def creer_agent(self, nom_utilisateur, mot_de_passe):
        raise NotImplemented

    @abstractmethod
    def modifier_agent(self):
        raise NotImplemented

    @abstractmethod
    def changer_droits(self):
        raise NotImplemented

    @abstractmethod
    def supprimer_agent(self):
        raise NotImplemented