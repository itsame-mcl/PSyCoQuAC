from DataLayer.DAO.db_connexion import DBConnexion
from DataLayer.DAO.interface_modele import InterfaceModele


class PGModele(InterfaceModele):
    @staticmethod
    def __pg_to_dao(data: dict) -> dict:
        data["position_champ_numero"] = tuple(data["position_champ_numero"])
        data["position_champ_voie"] = tuple(data["position_champ_voie"])
        data["position_champ_code_postal"] = tuple(data["position_champ_code_postal"])
        data["position_champ_ville"] = tuple(data["position_champ_ville"])
        sup_as_dict = {}
        for index in range(0, len(data["position_champs_supplementaires"]), 2):
            sup_as_dict[data["position_champs_supplementaires"][index]] =\
                data["position_champs_supplementaires"][index+1]
        data["position_champs_supplementaires"] = sup_as_dict
        return data

    @staticmethod
    def __dao_to_pg(data: dict) -> dict:
        data["position_champ_numero"] = list(data["position_champ_numero"])
        data["position_champ_voie"] = list(data["position_champ_voie"])
        data["position_champ_code_postal"] = list(data["position_champ_code_postal"])
        data["position_champ_ville"] = list(data["position_champ_ville"])
        sup_as_list = []
        for k, v in data["position_champs_supplementaires"].items():
            sup_as_list.extend([str(k), str(v)])
        data["position_champs_supplementaires"] = sup_as_list
        return data

    def recuperer_modele(self, identifiant: int) -> dict:
        with DBConnexion().connexion.cursor() as curseur:
            row = curseur.execute("SELECT * FROM modeles WHERE identifiant_modele=(%s)", (identifiant,)).fetchone()
        data = dict(zip(row.keys(), row))
        data = self.__pg_to_dao(data)
        return data

    def recuperer_regex(self) -> dict:
        with DBConnexion().connexion.cursor() as curseur:
            rows = curseur.execute("SELECT identifiant_modele, regex_nom_fichier FROM modeles").fetchall()
        answer = dict()
        for row in rows:
            answer[row["identifiant_modele"]] = row["regex_nom_fichier"]
        return answer

    def creer_modele(self, data: dict) -> bool:
        data = self.__dao_to_pg(data)
        try:
            with DBConnexion().connexion.cursor() as curseur:
                curseur.execute("""
                INSERT INTO modeles(nom_modele, regex_nom_fichier, position_champ_numero, position_champ_voie,
                position_champ_code_postal, position_champ_ville, position_champs_supplementaires)
                VALUES ((%s), (%s), (%s), (%s), (%s), (%s), (%s))
                """, (data['nom_modele'], data['regex_nom_fichier'], data['position_champ_numero'],
                      data['position_champ_voie'], data['position_champ_code_postal'], data['position_champ_ville'],
                      data['position_champs_supplementaires']))
            return True
        except Exception as e:
            print(e)
            return False

    def modifier_modele(self, data: dict) -> bool:
        data = self.__dao_to_pg(data)
        try:
            with DBConnexion().connexion.cursor() as curseur:
                curseur.execute("""
                UPDATE modeles SET nom_modele=(%s), regex_nom_fichier=(%s), position_champ_numero=(%s),
                position_champ_voie=(%s), position_champ_code_postal=(%s), position_champ_ville=(%s),
                position_champs_supplementaires=(%s)
                WHERE identifiant_modele=(%s)
                """, (data['nom_modele'], data['regex_nom_fichier'], data['position_champ_numero'],
                      data['position_champ_voie'], data['position_champ_code_postal'],
                      data['position_champ_ville'], data['position_champs_supplementaires'],
                      data['identifiant_modele']))
            return True
        except Exception as e:
            print(e)
            return False

    def supprimer_modele(self, identifiant: int) -> bool:
        try:
            with DBConnexion().connexion.cursor() as curseur:
                curseur.execute("DELETE FROM modeles WHERE identifiant_modele=(%s)", (identifiant,))
            return True
        except Exception as e:
            print(e)
            return False

    def recuperer_dernier_id_modele(self) -> int:
        with DBConnexion().connexion.cursor() as curseur:
            row = curseur.execute("SELECT last_value, is_called FROM modeles_identifiant_modele_seq").fetchone()
        if row["is_called"]:
            value = row["last_value"]
        else:
            value = row["last_value"] - 1
        return value
