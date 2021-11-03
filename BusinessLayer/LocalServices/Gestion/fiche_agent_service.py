from BusinessLayer.BusinessObjects.agent import Agent
from BusinessLayer.BusinessObjects.session import Session
from BusinessLayer.LocalServices.Gestion.fiche_superviseur import FicheSuperviseur
from BusinessLayer.LocalServices.Gestion.fiche_gestionnaire import FicheGestionnaire
from utils.singleton import Singleton

@Singleton
class AgentServices:

    def creer_agent(session_utilisateur : Session, prenom : varchar(50), nom : varchar(100), nom_utilisateur : varchar(20), mot_de_passe : char(128), est_superviseur : bool):
        if self.droits_superviseurs:
            self.__interface = FicheSuperviseur()
        else:
            self.__interface = FicheGestionnaire()
        return self.__interface.creer_agent(session_utilisateur, prenom, nom, nom_utilisateur, mot_de_passe, est_superviseur)

    def modifier_agent(self, agent_a_modifier : Agent, prenom : varchar(50), nom : varchar(100), mot_de_passe : char(128)):
        if self.droits_superviseurs:
            self.__interface = FicheSuperviseur()
        else:
            self.__interface = FicheGestionnaire()
        return self.__interface.modifier_agent(agent_a_modifier, prenom, nom, mot_de_passe)

    def changer_droits(self, agent_a_modifier : Agent):
        if self.droits_superviseurs:
            self.__interface = FicheSuperviseur()
        else:
            self.__interface = FicheGestionnaire()
        return self.__interface.changer_droits(agent_a_modifier)

    def supprimer_agent(self, agent_a_supprimer : Agent):
        if self.droits_superviseurs:
            self.__interface = FicheSuperviseur()
        else:
            self.__interface = FicheGestionnaire()
        return self.__interface.supprimer_agent(agent_a_supprimer)