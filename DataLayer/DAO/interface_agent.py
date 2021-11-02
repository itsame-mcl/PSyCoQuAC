from abc import ABC, abstractmethod

from BusinessLayer.BusinessObjects.agent import Agent

class InterfaceAgent(ABC):

    @abstractmethod
    def deleguer_agent_a(self, id_agents : List[int], id_superviseur_actuel : int, id_superviseur_futur : int):
        raise NotImplemented

    @abstractmethod
    def recuperer_liste_agents(self, id_superviseur : int) -> List[Agent]:
        raise NotImplemented

    @abstractmethod
    def creer_agent(self, session_utilisateur : Session, prenom : varchar(50), nom : varchar(100), nom_utilisateur : varchar(20), mot_de_passe : char(128), est_superviseur : bool):
        raise NotImplemented

    @abstractmethod
    def modifier_agent(self, agent_a_modifier : Agent) -> bool:
        raise NotImplemented

    @abstractmethod
    def changer_droit(self, agent_a_modifier : Agent) -> bool:
        raise NotImplemented

    @abstractmethod
    def supprimer_agent(self, id_agent : int) -> bool:
        raise NotImplemented

    @abstractmethod
    def est_superviseur(self, nom_utilisateur : varchar(20)) -> bool:
        raise NotImplemented

    @abstractmethod
    def recuperer_mdp_agent(self, nom_utilisateur : varchar(20), mot_de_passe : varchar(100)) -> char(128):
        raise NotImplemented