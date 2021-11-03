from ast import literal_eval

from DataLayer.DAO.db_connexion import DBConnexion
from DataLayer.DAO.interface_modele import InterfaceModele


class SQLiteModele(InterfaceModele):
    def __sqlite_to_dao(self, data: dict) -> dict:
        data["position_champs_supplementaires"] = literal_eval(data["position_champs_supplementaires"])
        return data

    def __dao_to_sqlite(self, data: dict) -> dict:
        data["position_champs_supplementaires"] = repr(data["position_champs_supplementaires"])
        return data

    def recuperer_modele(self, identifiant: int) -> dict:
        curseur = DBConnexion().connexion.cursor()
        curseur.execute("SELECT * FROM modeles WHERE identifiant_modele=:id", {"id": identifiant})
        row = curseur.fetchone()
        curseur.close()
        data: dict = dict(zip(row.keys(), row))
        data = self.__sqlite_to_dao(data)
        return data

    def recuperer_regex(self) -> dict:
        curseur = DBConnexion().connexion.cursor()
        curseur.execute("SELECT identifiant_modele, regex_nom_fichier FROM modeles")
        rows = curseur.fetchall()
        curseur.close()
        answer = dict()
        for row in rows:
            answer[row["identifiant_modele"]] = row["regex_nom_fichier"]
        return answer

    def creer_modele(self, data: dict) -> bool:
        data = self.__dao_to_sqlite(data)
        try:
            curseur = DBConnexion().connexion.cursor()
            curseur.execute("""
            INSERT INTO modeles(nom_modele, regex_nom_fichier, position_champ_numero, position_champ_voie,
            position_champ_code_postal, position_champ_ville, position_champs_supplementaires)
            VALUES (:nom_modele, :regex_nom_fichier, :position_champ_numero, :position_champ_voie,
            :position_champ_code_postal, :position_champ_ville, :position_champs_supplementaires)
            """, data)
            DBConnexion().connexion.commit()
            curseur.close()
            return True
        except Exception as e:
            print(e)
            return False

    def modifier_modele(self, data: dict) -> bool:
        data = self.__dao_to_sqlite(data)
        try:
            curseur = DBConnexion().connexion.cursor()
            curseur.execute("""
            UPDATE modeles SET nom_modele=:nom_modele, regex_nom_fichier=:regex_nom_fichier,
            position_champ_numero=:position_champ_numero, position_champ_voie=:position_champ_voie,
            position_champ_code_postal=:position_champ_code_postal, position_champ_ville=:position_champ_ville,
            position_champs_supplementaires=:position_champs_supplementaires
            WHERE identifiant_modele=:identifiant_modele
            """, data)
            DBConnexion().connexion.commit()
            curseur.close()
            return True
        except Exception as e:
            print(e)
            return False

    def supprimer_modele(self, identifiant: int) -> bool:
        try:
            curseur = DBConnexion().connexion.cursor()
            curseur.execute("DELETE FROM modeles WHERE identifiant_modele=:id", {"id": identifiant})
            DBConnexion().connexion.commit()
            curseur.close()
            return True
        except Exception as e:
            print(e)
            return False
