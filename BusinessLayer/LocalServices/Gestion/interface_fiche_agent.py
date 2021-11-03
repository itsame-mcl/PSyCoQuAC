from abc import ABC, abstractmethod
from BusinessLayer.BusinessObjects.agent import Agent
from BusinessLayer.BusinessObjects.session import Session

class InterfaceFicheAgent(ABC):

    @abstractmethod
    def creer_agent(self, prenom : varchar(50), nom : varchar(100), nom_utilisateur : varchar(20), mot_de_passe : char(128)):
        raise NotImplemented

    @abstractmethod
    def modifier_agent(self, agent_a_modifier : Agent, prenom : varchar(50), nom : varchar(100), mot_de_passe : char(128)):
        raise NotImplemented

    @abstractmethod
    def changer_droits(self, agent_a_modifier: Agent):
        raise NotImplemented

    @abstractmethod
    def supprimer_agent(self, agent_a_supprimer : Agent):
        raise NotImplemented