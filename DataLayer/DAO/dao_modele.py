import dotenv

from BusinessLayer.BusinessObjects.modele import Modele
from DataLayer.DAO.sqlite_modele import SQLiteModele
from utils.singleton import Singleton


class DAOModele(metaclass=Singleton):
    def __init__(self):
        engine = dotenv.dotenv_values(".env")["ENGINE"]
        if engine == "SQLite":
            self.__interface = SQLiteModele()

    def creer_modele(self, modele : Modele) -> bool:
        pass