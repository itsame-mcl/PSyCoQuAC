from BusinessLayer.BusinessObjects.agent import Agent
from BusinessLayer.LocalServices.Gestion.interface_fiche_agent import InterfaceFicheAgent
from DataLayer.DAO.dao_agent import DAOAgent

class FicheGestionnaire(InterfaceFicheAgent):

    def creer_agent(self, est_superviseur : bool, quotite : float, id_superviseur : int, nom_utilisateur : str, mot_de_passe : str, prenom : str, nom : str) -> bool:
        return DAOAgent.creer_agent(est_superviseur, quotite, id_superviseur, nom_utilisateur, mot_de_passe, prenom, nom)

    def modifier_agent(self, agent_a_modifier : Agent, data : dict) -> bool:
        return DAOAgent.modifier_agent(agent_a_modifier, data)

    def changer_droits(self, agent_a_modifier : Agent) -> bool: # On change le Gestionnaire en Superviseur
        return DAOAgent.changer_droits(agent_a_modifier)

    def supprimer_agent(self, agent_a_supprimer : Agent) -> bool:
        return DAOAgent.supprimer_agent(agent_a_supprimer.agent_id)