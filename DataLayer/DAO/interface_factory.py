import os
import dotenv

from DataLayer.DAO.sqlite_connexion import SQLiteConnexion
from DataLayer.DAO.sqlite_fiche_adresse import SQLiteFicheAdresse
from DataLayer.DAO.sqlite_modele import SQLiteModele
from DataLayer.DAO.sqlite_agent import SQLiteAgent
from DataLayer.DAO.pg_connexion import PGConnexion


class InterfaceFactory:
    @staticmethod
    def get_interface(type_dao: str):
        dotenv.load_dotenv(override=True)
        if os.environ["ENGINE"] == "SQLite":
            if type_dao == "Connexion":
                return SQLiteConnexion()
            elif type_dao == "FicheAdresse":
                return SQLiteFicheAdresse()
            elif type_dao == "Modele":
                return SQLiteModele()
            elif type_dao == "Agent":
                return SQLiteAgent()
            else:
                raise NotImplementedError
        elif os.environ["ENGINE"] == "PostgreSQL":
            if type_dao == "Connexion":
                return PGConnexion()
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError
