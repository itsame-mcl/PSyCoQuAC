from BusinessLayer.BusinessObjects.agent import Agent
from BusinessLayer.BusinessObjects.session import Session
from BusinessLayer.LocalServices.Gestion.interface_fiche_agent import InterfaceFicheAgent
from DataLayer import DAO as dao

class FicheSuperviseur(InterfaceFicheAgent):

    def creer_agent(self, session_utilisateur : Session, prenom : varchar(50), nom : varchar(100), nom_utilisateur : varchar(20), mot_de_passe : char(128), est_superviseur : bool) -> bool:
        return dao.DAOAgent.creer_agent(session_utilisateur, prenom, nom, nom_utilisateur, mot_de_passe, est_superviseur)

    def modifier_agent(self, agent_a_modifier : Agent, prenom : varchar(50), nom : varchar(100), mot_de_passe : char(128)) -> bool:
        return dao.DAOAgent.modifier_agent(agent_a_modifier)

    def changer_droits(self, agent_a_modifier : Agent) -> bool: # On change le Superviseur en Gestionnaire
        return dao.DAOAgent.changer_droits(agent_a_modifier)

    def supprimer_agent(self, agent_a_supprimer : Agent) -> bool:
        return dao.DAOAgent.supprimer_agent(agent_a_supprimer.agent_id)