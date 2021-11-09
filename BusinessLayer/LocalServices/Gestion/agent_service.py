from BusinessLayer.BusinessObjects.agent import Agent
from BusinessLayer.BusinessObjects.session import Session
from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from DataLayer.DAO.dao_agent import DAOAgent
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
from utils.singleton import Singleton
from typing import List

@Singleton
class AgentService:

    def creer_agent(self, est_superviseur : bool, quotite : float, id_superviseur : int, nom_utilisateur : str, mot_de_passe : str, prenom : str, nom : str) -> bool:
        return DAOAgent.creer_agent(est_superviseur, quotite, id_superviseur, nom_utilisateur, mot_de_passe, prenom, nom)

    def modifier_agent(self, agent_a_modifier : dict) -> bool: 
        return DAOAgent.modifier_agent(agent_a_modifier)

    def changer_droits(self, id_agent : int) -> bool:
        agent_a_modifier = DAOAgent.recuperer_agent(id_agent)
        return DAOAgent.changer_droits(agent_a_modifier)

    def supprimer_agent(self, agent_a_supprimer : Agent) -> bool:
        return DAOAgent.supprimer_agent(agent_a_supprimer.agent_id)

    def saler_hasher_mdp(self, nom_utilisateur : str, mot_de_passe : str) -> str:
        return DAOAgent.__saler_hasher_mdp(nom_utilisateur, mot_de_passe)
    
    def recuperer_id_superviseur(self, id_agent : int) -> int:
        return DAOAgent.recuperer_id_superviseur(id_agent)['id_superviseur']
        
    def recuperer_equipe(self, session_supervsieur : Session) -> List[Agent]:
        return DAOAgent.recuperer_equipe(session_supervsieur.utilisateur_connecte.agent_id)

    def recuperer_pot(self, id_agent : int) -> List[FicheAdresse]:
        return DAOFicheAdresse.recuperer_pot(id_agent)