from BusinessLayer.BusinessObjects.Agent import Agent
import DataLayer.DAO as dao
from utils.singleton import Singleton

@Singleton
class AgentServices:

    def creer_agent(Session session_utilisateur, string prenom, string nom, string nom_utilisateur, string mot_de_passe, bool est_superviseur):


    def modifier_agent(Session session_utilsateur, Agent agent_a_modifier,string prenom, string nom, string mot_de_passe):


    def changer_droits(Session session_utilisateur,Agent agent_a_modifier):
        

    def supprimer_agent(Session session_utilisateur,Agent agent_a_supprimer):