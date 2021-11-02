
from DataLayer.DAO.db_connexion import DBConnexion
from DataLayer.DAO.interface_fiche_adresse import InterfaceFicheAdresse


class SQLiteFicheAdresse(InterfaceFicheAdresse):
    def recuperer_fiche_adresse(self, identifiant):
        curseur = DBConnexion.connexion.cursor()
        curseur.execute("SELECT * FROM fa WHERE identifiant_fa=:id", {"id": identifiant})
        row = curseur.fetchone()
        data = dict(zip(row.keys(), row))
        return data
