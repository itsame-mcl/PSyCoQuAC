import dotenv

from BusinessLayer.BusinessObjects.agent import Agent
from DataLayer.DAO.sqlite_agent import SQLiteAgent
from utils.singleton import Singleton


class DAOAgent(metaclass=Singleton):

    def __init__(self):
        engine = dotenv.dotenv_values(".env")["ENGINE"]
        if engine == "SQLite":
            self.__interface = SQLiteAgent()

    def deleguer_agent_a(self, id_agents : List[int], id_superviseur_actuel : int, id_superviseur_futur : int) -> bool:
        res = self.__interface.deleguer_agent_a(id_agent, id_superviseur_actuel, id_superviseur_futur)
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