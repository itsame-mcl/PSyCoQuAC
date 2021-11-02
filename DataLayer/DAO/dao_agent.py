import dotenv

from BusinessLayer.BusinessObjects.agent import Agent
from DataLayer.DAO.sqlite_agent import SQLiteAgent
from utils.singleton import Singleton


class DAOAgent(metaclass=Singleton):

    def __init__(self):
        engine = dotenv.dotenv_values(".env")["ENGINE"]
        if engine == "SQLite":
            self.__interface = SQLiteAgent()

    def deleguer_agent_a(self, id_agents : List[int], id_superviseur : int) -> bool:
        res = self.__interface.deleguer_agent_a(id_agents, id_superviseur)
        return res

    def recuperer_fiches_agent(self, id_agent : int) -> List[dict]:
        res = self.__interface.recuperer_fiches_agent(id_agent)
        return res

    def recuperer_liste_agents(self, id_superviseur : int) -> List[Agent]:
        res = self.__interface.recuperer_liste_agents(id_superviseur)
        return res

    def supprimer_agent(self, id_agent : int) -> bool:
        res = self.__interface.supprimer_agent(id_agent)
        return res

    def creer_agent(self, session_utilisateur : Session, prenom : varchar(50), nom : varchar(100), nom_utilisateur : varchar(20), mot_de_passe : char(128), est_superviseur : bool):
        res = self.__interface.creer_agent(session_utilisateur, prenom, nom, nom_utilisateur, mot_de_passe, est_superviseurr)
        return res

    def modifier_agent(self, agent_a_modifier : Agent) -> bool:
        res = self.__interface.modifier_agent(agent_a_modifier)
        return res

    def changer_droit(self, agent_a_modifier : Agent) -> bool:
        res = self.__interface.changer_droit(agent_a_modifier)
        return res

    def est_superviseur(self, nom_utilisateur : varchar(20)) -> bool:
        res = self.__interface.est_superviseur(nom_utilisateur)
        return res

    def recuperer_mdp_agent(self, nom_utilisateur : varchar(20), mot_de_passe : varchar(100)) -> char(128):
        res = self.__interface.recuperer_mdp_agent(nom_utilisateur, mot_de_passe)
        return res