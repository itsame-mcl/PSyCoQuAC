from BusinessLayer.LocalServices.Gestion.interface_fiche_agent import InterfaceFicheAgent

class FicheSuperviseur(InterfaceFicheAgent):

    def creer_agent(self, nom_utilisateur, mot_de_passe):
        raise NotImplemented

    def modifier_agent(self):
        raise NotImplemented

    def changer_droits(self, agent_a_modifier): # On change le Superviseur en Gestionnaire
        agent_a_modifier.

    def supprimer_agent(self):
        raise NotImplemented