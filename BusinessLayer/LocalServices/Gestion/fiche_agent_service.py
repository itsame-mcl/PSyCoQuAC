from BusinessLayer.BusinessObjects.agent import Agent
from BusinessLayer.LocalServices.Gestion.fiche_superviseur import FicheSuperviseur
from BusinessLayer.LocalServices.Gestion.fiche_gestionnaire import FicheGestionnaire
from utils.singleton import Singleton

@Singleton
class AgentServices:

    def creer_agent(self, est_superviseur : bool, quotite : float, id_superviseur : int, nom_utilisateur : str, mot_de_passe : str, prenom : str, nom : str) -> bool:
        if self.droits_superviseurs:
            self.__interface = FicheSuperviseur()
        else:
            self.__interface = FicheGestionnaire()
        return self.__interface.creer_agent(est_superviseur, quotite, id_superviseur, nom_utilisateur, mot_de_passe, prenom, nom)

    def modifier_agent(self, agent_a_modifier : Agent, data : dict) -> bool:
        if self.droits_superviseurs:
            self.__interface = FicheSuperviseur()
        else:
            self.__interface = FicheGestionnaire()
        return self.__interface.modifier_agent(agent_a_modifier, data)

    def changer_droits(self, agent_a_modifier : Agent) -> bool:
        if self.droits_superviseurs:
            self.__interface = FicheSuperviseur()
        else:
            self.__interface = FicheGestionnaire()
        return self.__interface.changer_droits(agent_a_modifier)

    def supprimer_agent(self, agent_a_supprimer : Agent) -> bool:
        if self.droits_superviseurs:
            self.__interface = FicheSuperviseur()
        else:
            self.__interface = FicheGestionnaire()
        return self.__interface.supprimer_agent(agent_a_supprimer)