from BusinessLayer.LocalServices.Gestion.interface_fiche_agent import InterfaceFicheAgent
from DataLayer import DAO as dao

class FicheGestionnaire(InterfaceFicheAgent):

    def creer_agent(self, session_utilisateur, prenom, nom, nom_utilisateur, mot_de_passe, est_superviseur):
        raise NotImplemented

    def modifier_agent(self, agent_a_modifier, prenom, nom, mot_de_passe):
        raise NotImplemented

    def changer_droits(self, agent_a_modifier): # On change le Gestionnaire en Superviseur
        dao.from_gestionnaire_to_superviseur(agent_a_modifier)

    def supprimer_agent(self, agent_a_supprimer):
        raise NotImplemented