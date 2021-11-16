import os
import dotenv


import DataLayer.DAO.sqlite_connexion as slcx
import DataLayer.DAO.sqlite_fiche_adresse as slfa
import DataLayer.DAO.sqlite_modele as slmo
import DataLayer.DAO.sqlite_agent as slag
import DataLayer.DAO.pg_connexion as pgcx


class InterfaceFactory:
    @staticmethod
    def get_interface(type_dao: str):
        dotenv.load_dotenv(override=True)
        if os.environ["ENGINE"] == "SQLite":
            if type_dao == "Connexion":
                return slcx.SQLiteConnexion()
            elif type_dao == "FicheAdresse":
                return slfa.SQLiteFicheAdresse()
            elif type_dao == "Modele":
                return slmo.SQLiteModele()
            elif type_dao == "Agent":
                return slag.SQLiteAgent()
            else:
                raise NotImplementedError
        elif os.environ["ENGINE"] == "PostgreSQL":
            if type_dao == "Connexion":
                return pgcx.PGConnexion()
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError
