from typing import List
from psycopg.rows import tuple_row
from DataLayer.DAO.db_connexion import DBConnexion
from DataLayer.DAO.interface_fiche_adresse import InterfaceFicheAdresse


class PGFicheAdresse(InterfaceFicheAdresse):
    @staticmethod
    def __pg_to_dao(data: dict) -> dict:
        data["coordonnees_wgs84"] = tuple([str(coord) for coord in (data["coordonnees_wgs84"])])
        if data["champs_supplementaires"] is not None:
            sup_as_dict = {}
            for index in range(0, len(data["champs_supplementaires"]), 2):
                sup_as_dict[data["champs_supplementaires"][index]] = data["champs_supplementaires"][index+1]
            data["champs_supplementaires"] = sup_as_dict
        return data

    @staticmethod
    def __dao_to_pg(data: dict) -> dict:
        data["coordonnees_wgs84"] = [float(coord) for coord in (data["coordonnees_wgs84"])]
        if data["champs_supplementaires"] is not None:
            sup_as_list = []
            for k, v in data["champs_supplementaires"].items():
                sup_as_list.extend([str(k), str(v)])
            data["champs_supplementaires"] = sup_as_list
        return data

    def recuperer_fiche_adresse(self, identifiant: int) -> dict:
        with DBConnexion().connexion.cursor() as curseur:
            row = curseur.execute("SELECT * FROM fa WHERE identifiant_fa=(%s)", (identifiant,)).fetchone()
        data = self.__pg_to_dao(row)
        return data

    def recuperer_liste_fiches_adresse(self, id_agent: int, id_lot: int) -> List[dict]:
        if id_agent > 0 > id_lot:
            params = (id_agent,)
            request = "SELECT * FROM fa WHERE identifiant_pot=(%s) ORDER BY identifiant_fa"
        elif id_agent < 0 < id_lot:
            params = (id_lot,)
            request = "SELECT * FROM fa WHERE identifiant_lot=(%s) ORDER BY identifiant_fa"
        elif id_agent > 0 and id_lot > 0:
            params = (id_agent, id_lot)
            request = "SELECT * FROM fa WHERE identifiant_pot=(%s) AND identifiant_lot=(%s) ORDER BY identifiant_fa"
        else:
            params = ()
            request = "SELECT * FROM fa ORDER BY identifiant_fa"
        with DBConnexion().connexion.cursor() as curseur:
            rows = curseur.execute(request, params).fetchall()
        answer = list()
        for row in rows:
            data = self.__pg_to_dao(row)
            answer.append(data)
        return answer

    def creer_fiche_adresse(self, data: dict) -> bool:
        data = self.__dao_to_pg(data)
        try:
            with DBConnexion().connexion.cursor() as curseur:
                curseur.execute("""
                INSERT INTO fa(identifiant_pot, identifiant_lot, code_resultat, date_importation,
                date_dernier_traitement, initial_numero, initial_voie, initial_code_postal, initial_ville, final_numero,
                final_voie, final_code_postal, final_ville, coordonnees_wgs84, champs_supplementaires)
                VALUES((%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s))
                """, (data['identifiant_pot'], data['identifiant_lot'], data['code_resultat'], data['date_importation'],
                      data['date_dernier_traitement'], data['initial_numero'], data['initial_voie'],
                      data['initial_code_postal'], data['initial_ville'], data['final_numero'], data['final_voie'],
                      data['final_code_postal'], data['final_ville'], data['coordonnees_wgs84'],
                      data['champs_supplementaires']))
            return True
        except Exception as e:
            print(e)
            return False

    def creer_multiple_fiche_adresse(self, data: List[dict]) -> bool:
        data_pg = [self.__dao_to_pg(item) for item in data]
        copy_list = [[data['identifiant_pot'], data['identifiant_lot'], data['code_resultat'], data['date_importation'],
                      data['date_dernier_traitement'], data['initial_numero'], data['initial_voie'],
                      data['initial_code_postal'], data['initial_ville'], data['final_numero'], data['final_voie'],
                      data['final_code_postal'], data['final_ville'], data['coordonnees_wgs84'],
                      data['champs_supplementaires']] for data in data_pg]
        try:
            with DBConnexion().connexion.cursor().copy("""COPY fa(identifiant_pot, identifiant_lot, code_resultat,
            date_importation, date_dernier_traitement, initial_numero, initial_voie, initial_code_postal, initial_ville,
            final_numero, final_voie, final_code_postal, final_ville,
            coordonnees_wgs84, champs_supplementaires) FROM STDIN""") as curseur:
                for line in copy_list:
                    curseur.write_row(line)
            return True
        except Exception as e:
            print(e)
            return False

    def modifier_fiche_adresse(self, data: dict) -> bool:
        data = self.__dao_to_pg(data)
        try:
            with DBConnexion().connexion.cursor() as curseur:
                curseur.execute("""
                UPDATE fa SET identifiant_pot=(%s), identifiant_lot=(%s), code_resultat=(%s),
                date_dernier_traitement=(%s), final_numero=(%s), final_voie=(%s), final_code_postal=(%s),
                final_ville=(%s), coordonnees_wgs84=(%s), champs_supplementaires=(%s)
                WHERE identifiant_fa=(%s)
                """, (data['identifiant_pot'], data['identifiant_lot'], data['code_resultat'],
                      data['date_dernier_traitement'], data['final_numero'], data['final_voie'],
                      data['final_code_postal'], data['final_ville'], data['coordonnees_wgs84'],
                      data['champs_supplementaires'], data['identifiant_fa']))
            return True
        except Exception as e:
            print(e)
            return False

    def modifier_agent_fiches_adresse(self, id_agent: int, code_res: str, id_fas: List[int]) -> bool:
        try:
            with DBConnexion().connexion.cursor() as curseur:
                curseur.execute("UPDATE fa SET identifiant_pot=(%s), code_resultat=(%s) WHERE identifiant_fa = ANY(%s)",
                                (id_agent, code_res, id_fas))
            return True
        except Exception as e:
            print(e)
            return False

    def supprimer_fiche_adresse(self, identifiant: int) -> bool:
        try:
            with DBConnexion().connexion.cursor() as curseur:
                curseur.execute("DELETE FROM fa WHERE identifiant_fa=(%s)", (identifiant,))
            return True
        except Exception as e:
            print(e)
            return False

    def obtenir_statistiques(self, criteria: list) -> List[tuple]:
        request = self._obtenir_statistiques_request_helper(criteria)
        with DBConnexion().connexion.cursor(row_factory=tuple_row) as curseur:
            rows = curseur.execute(request).fetchall()
        answer = list()
        for row in rows:
            answer.append(tuple(row))
        return answer

    def recuperer_dernier_id_fa(self) -> int:
        with DBConnexion().connexion.cursor() as curseur:
            row = curseur.execute("SELECT last_value, is_called FROM fa_identifiant_fa_seq").fetchone()
        if row["is_called"]:
            value = row["last_value"]
        else:
            value = row["last_value"] - 1
        return value

    def recuperer_dernier_id_lot(self) -> int:
        with DBConnexion().connexion.cursor() as curseur:
            row = curseur.execute("SELECT last_value, is_called FROM identifiant_lot_seq").fetchone()
        if row["is_called"]:
            value = row["last_value"]
        else:
            value = row["last_value"] - 1
        return value

    def incrementer_id_lot(self) -> bool:
        try:
            with DBConnexion().connexion.cursor() as curseur:
                curseur.execute("SELECT nextval('identifiant_lot_seq')")
            return True
        except Exception as e:
            print(e)
            return False
