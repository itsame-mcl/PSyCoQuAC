import psycopg as pg
from psycopg.rows import dict_row
from DataLayer.DAO.interface_connexion import InterfaceConnexion


class PGConnexion(InterfaceConnexion):

    def ouvrir_connexion(self, host, port, database, user, password):
        try:
            connexion = pg.connect(host=host,
                                   port=port,
                                   database=database,
                                   user=user,
                                   password=password,
                                   row_factory=dict_row,
                                   autocommit=True)
            return connexion
        except Exception as e:
            raise e

    def fermer_connexion(self, connexion):
        connexion.close()
