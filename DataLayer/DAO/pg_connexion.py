import psycopg as pg
from psycopg.rows import dict_row
from DataLayer.DAO.interface_connexion import InterfaceConnexion


class PGConnexion(InterfaceConnexion):

    def ouvrir_connexion(self, host, port, database, user, password):
        try:
            connexion_string = "host=" + str(host) + " port=" + str(port) + " dbname=" + str(database) +\
                               " user=" + str(user) + " password=" + str(password)
            connexion = pg.connect(conninfo=connexion_string,
                                   row_factory=dict_row,
                                   autocommit=True)
            return connexion
        except Exception as e:
            print(e)
            return None

    def fermer_connexion(self, connexion):
        connexion.close()
