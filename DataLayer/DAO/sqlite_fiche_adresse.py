from ast import literal_eval
from datetime import datetime
from typing import List

from DataLayer.DAO.db_connexion import DBConnexion
from DataLayer.DAO.interface_fiche_adresse import InterfaceFicheAdresse

class SQLiteFicheAdresse(InterfaceFicheAdresse):
    
    def __sqlite_to_dao(self, data: dict) -> dict:
        data["date_importation"] = datetime.fromisoformat(data["date_importation"]).date()
        data["date_dernier_traitement"] = datetime.fromisoformat(data["date_dernier_traitement"]).date()
        data["coordonnees_wgs84"] = literal_eval(data["coordonnees_wgs84"])
        data["champs_supplementaires"] = literal_eval(data["champs_supplementaires"])
        return data

    def __dao_to_sqlite(self, data: dict) -> dict:
        data["date_importation"] = str(data["date_importation"])
        data["date_dernier_traitement"] = str(data["date_dernier_traitement"])
        data["coordonnees_wgs84"] = repr(data["coordonnees_wgs84"])
        data["champs_supplementaires"] = repr(data["champs_supplementaires"])
        return data

    def recuperer_fiche_adresse(self, identifiant: int) -> dict:
        curseur = DBConnexion().connexion.cursor()
        curseur.execute("SELECT * FROM fa WHERE identifiant_fa=:id", {"id": identifiant})
        row = curseur.fetchone()
        curseur.close()
        data: dict = dict(zip(row.keys(), row))
        data = self.__sqlite_to_dao(data)
        return data

    def recuperer_liste_fiches_adresse(self, id_agent: int, id_lot: int) -> List[dict]:
        if id_agent > 0 and id_lot < 0:
            request = "SELECT * FROM fa WHERE identifiant_pot=:id_agent"
        elif id_agent < 0 and id_lot > 0:
            request = "SELECT * FROM fa WHERE identifiant_lot=:id_lot"
        elif id_agent > 0 and id_lot > 0:
            request = "SELECT * FROM fa WHERE identifiant_pot=:id_agent AND identifiant_lot=:id_lot"
        else:
            request = "SELECT * FROM fa"
        curseur = DBConnexion().connexion.cursor()
        curseur.execute(request, {"id_agent": id_agent})
        rows = curseur.fetchall()
        curseur.close()
        answer = list()
        for row in rows:
            data: dict = dict(zip(row.keys(), row))
            data = self.__sqlite_to_dao(data)
            answer.append(data)
        return answer

    def creer_fiche_adresse(self, data: dict) -> bool:
        data = self.__dao_to_sqlite(data)
        try:
            curseur = DBConnexion().connexion.cursor()
            curseur.execute("""
            INSERT INTO fa(identifiant_pot, identifiant_lot, code_resultat, date_importation,date_dernier_traitement,
            initial_numero, initial_voie, initial_code_postal, initial_ville,final_numero, final_voie,
            final_code_postal, final_ville, coordonnees_wgs84, champs_supplementaires)
            VALUES(:identifiant_pot, :identifiant_lot, :code_resultat, :date_importation, :date_dernier_traitement,
            :initial_numero, :initial_voie, :initial_code_postal, :initial_ville, :final_numero, :final_voie,
            :final_code_postal, :final_ville, :coordonnees_wgs84, :champs_supplementaires)
            """, data)
            DBConnexion().connexion.commit()
            curseur.close()
            return True
        except Exception as e:
            print(e)
            return False

    def modifier_fiche_adresse(self, data: dict) -> bool:
        data = self.__dao_to_sqlite(data)
        try:
            curseur = DBConnexion().connexion.cursor()
            curseur.execute("""
            UPDATE fa SET identifiant_pot=:identifiant_pot, identifiant_lot=:identifiant_lot,
            code_resultat=:code_resultat, date_dernier_traitement=:date_dernier_traitement,
            final_numero=:final_numero, final_voie=:final_voie, final_code_postal=:final_code_postal,
            final_ville=:final_ville, coordonnees_wgs84=:coordonnees_wgs84,
            champs_supplementaires=:champs_supplementaires
            WHERE identifiant_fa=:identifiant_fa
            """, data)
            DBConnexion().connexion.commit()
            curseur.close()
            return True
        except Exception as e:
            print(e)
            return False

    def modifier_agent_fiches_adresse(self, id_agent : int, id_fas : List[int]) -> bool:
        request = "UPDATE fa SET identifiant_pot=:id_agent WHERE identifiant_fa IN ({})".format(','.join(':{}'.format(i) for i in range(len(id_fas))))
        params = {"id_agent": id_agent}
        params.update({str(i): id for i, id in enumerate(id_fas)})
        try:
            curseur = DBConnexion().connexion.cursor()
            curseur.execute(request, params)
            DBConnexion().connexion.commit()
            curseur.close()
            return True
        except Exception as e:
            print(e)
            return False

    def supprimer_fiche_adresse(self, identifiant: int) -> bool:
        try:
            curseur = DBConnexion().connexion.cursor()
            curseur.execute("DELETE FROM fa WHERE identifiant_fa=:id", {"id": identifiant})
            DBConnexion().connexion.commit()
            curseur.close()
            return True
        except Exception as e:
            print(e)
            return False