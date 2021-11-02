from BusinessLayer.LocalServices.Gestion.fiche_superviseur import FicheSuperviseur
from BusinessLayer.LocalServices.Gestion.fiche_gestionnaire import FicheGestionnaire
from utils.singleton import Singleton

@Singleton
class AgentServices: # S'applique sur un Agent

    def creer_agent(session_utilisateur, prenom, nom, nom_utilisateur, mot_de_passe, est_superviseur):
        if self.droits_superviseurs:
            self.__interface = FicheSuperviseur()
        else:
            self.__interface = FicheGestionnaire()
        return self.__interface.creer_agent(session_utilisateur, prenom, nom, nom_utilisateur, mot_de_passe, est_superviseur)

    def modifier_agent(self, agent_a_modifier, prenom, nom, mot_de_passe):
        if self.droits_superviseurs:
            self.__interface = FicheSuperviseur()
        else:
            self.__interface = FicheGestionnaire()
        return self.__interface.modifier_agent(agent_a_modifier, prenom, nom, mot_de_passe)

    def changer_droits(self, agent_a_modifier):
        if self.droits_superviseurs:
            self.__interface = FicheSuperviseur()
        else:
            self.__interface = FicheGestionnaire()
        return self.__interface.changer_droits(agent_a_modifier)

    def supprimer_agent(self, agent_a_supprimer):
        if self.droits_superviseurs:
            self.__interface = FicheSuperviseur()
        else:
            self.__interface = FicheGestionnaire()
        return self.__interface.supprimer_agent(agent_a_supprimer)