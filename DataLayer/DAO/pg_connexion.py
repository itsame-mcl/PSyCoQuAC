import psycopg
from DataLayer.DAO.interface_connexion import InterfaceConnexion


class PGConnexion(InterfaceConnexion):

    def ouvrir_connexion(self, host, port, database, user, password):
        try:
            connexion = psycopg.connect(host=host,
                                        port=port,
                                        database=database,
                                        user=user,
                                        password=password)
            return connexion
        except Exception as e:
            raise e

    def fermer_connexion(self, connexion):
        connexion.close()
