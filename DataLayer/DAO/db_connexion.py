import os
import dotenv

from DataLayer.DAO.pg_connexion import PGConnexion
from DataLayer.DAO.sqlite_connexion import SQLiteConnexion
from utils.singleton import Singleton


class DBConnexion(metaclass=Singleton):
    def __init__(self):
        dotenv.load_dotenv(override=True)
        if os.environ["ENGINE"] == "SQLite":
            self.__interface = SQLiteConnexion()
        elif os.environ["ENGINE"] == "PostgreSQL":
            self.__interface = PGConnexion()
        self.__connexion = self.__interface.ouvrir_connexion(os.environ["HOST"], os.environ["PORT"],
                                                             os.environ["DATABASE"],
                                                             os.environ["USER"], os.environ["PASSWORD"])
        if self.__connexion is None:
            raise ConnectionError

    @property
    def connexion(self):
        """
        return the opened connection.

        :return: the opened connection.
        """
        return self.__connexion

    def __del__(self):
        self.__interface.fermer_connexion(self.__connexion)
