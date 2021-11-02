import psycopg2
from psycopg2.extras import RealDictCursor
from DataLayer.DAO.interface_connexion import InterfaceConnexion


class PGConnexion(InterfaceConnexion):
    def ouvrir_connexion(self, host, port, database, user, password):
        try:
            connexion = psycopg2.connect(host=host,
                                         port=port,
                                         database=database,
                                         user=user,
                                         password=password,
                                         cursor_factory=RealDictCursor)
        except:
            connexion = None
        return connexion

    def fermer_connexion(self, connexion):
        connexion.close()
