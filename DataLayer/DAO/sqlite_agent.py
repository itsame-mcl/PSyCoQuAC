from typing import List
from DataLayer.DAO.db_connexion import DBConnexion
from DataLayer.DAO.interface_agent import InterfaceAgent


class SQLiteAgent(InterfaceAgent):

    @staticmethod
    def __sqlite_to_dao(data: dict) -> dict:
        data["est_superviseur"] = bool(data["est_superviseur"])
        return data

    @staticmethod
    def __dao_to_sqlite(data: dict):
        data["est_superviseur"] = int(data["est_superviseur"])
        return data

    def recuperer_agent(self, id_agent: int) -> dict:
        curseur = DBConnexion().connexion.cursor()
        curseur.execute("SELECT * FROM agents WHERE identifiant_agent=:id", {"id": id_agent})
        row = curseur.fetchone()
        curseur.close()
        data = dict(zip(row.keys(), row))
        data = self.__sqlite_to_dao(data)
        return data

    def recuperer_liste_agents(self, id_superviseur: int) -> List[dict]:
        if id_superviseur > 0:
            request = "SELECT * FROM agents WHERE identifiant_superviseur =:id_superviseur"
        else:
            request = "SELECT * FROM agents"
        curseur = DBConnexion().connexion.cursor()
        curseur.execute(request, {"id_superviseur": id_superviseur})
        rows = curseur.fetchall()
        curseur.close()
        answer = list()
        for row in rows:
            data = dict(zip(row.keys(), row))
            data = self.__sqlite_to_dao(data)
            answer.append(data)
        return answer

    def supprimer_agent(self, id_agent: int) -> bool:
        try:
            curseur = DBConnexion().connexion.cursor()
            curseur.execute("DELETE FROM agents WHERE identifiant_agent=:id", {"id": id_agent})
            DBConnexion().connexion.commit()
            curseur.close()
            return True
        except Exception as e:
            print(e)
            return False

    def creer_agent(self, data: dict) -> bool:
        data = self.__dao_to_sqlite(data)
        try:
            curseur = DBConnexion().connexion.cursor()
            curseur.execute("""
            INSERT INTO agents (est_superviseur, quotite, identifiant_superviseur,
            nom_utilisateur, mot_de_passe, prenom, nom)
            VALUES(:est_superviseur, :quotite, :identifiant_superviseur, :nom_utilisateur,
            :mot_de_passe, :prenom, :nom)
            """, data)
            DBConnexion().connexion.commit()
            curseur.close()
            return True
        except Exception as e:
            print(e)
            return False

    def modifier_agent(self, data: dict) -> bool:
        data = self.__dao_to_sqlite(data)
        try:
            curseur = DBConnexion().connexion.cursor()
            curseur.execute("""
            UPDATE agents SET est_superviseur=:est_superviseur, quotite=:quotite,
            identifiant_superviseur=:identifiant_superviseur, prenom=:prenom, nom=:nom
            WHERE identifiant_agent=:identifiant_agent
            """, data)
            DBConnexion().connexion.commit()
            curseur.close()
            return True
        except Exception as e:
            print(e)
            return False

    def modifier_superviseur(self, id_agents: List[int], id_superviseur: int) -> bool:
        request = "UPDATE agents SET identifiant_superviseur=:id_superviseur WHERE identifiant_agent IN ({})".format(
            ','.join(':{}'.format(i) for i in range(len(id_agents))))
        params = {"id_superviseur": id_superviseur}
        params.update({str(i): id_agent for i, id_agent in enumerate(id_agents)})
        try:
            curseur = DBConnexion().connexion.cursor()
            curseur.execute(request, params)
            DBConnexion().connexion.commit()
            curseur.close()
            return True
        except Exception as e:
            print(e)
            return False

    def promouvoir_agent(self, agent_a_promouvoir: int) -> bool:
        try:
            curseur = DBConnexion().connexion.cursor()
            curseur.execute("""
            UPDATE agents SET est_superviseur=1, identifiant_superviseur=:id_agent WHERE identifiant_agent=:id_agent
            """, {'id_agent': agent_a_promouvoir})
            DBConnexion().connexion.commit()
            curseur.close()
            return True
        except Exception as e:
            print(e)
            return False

    def connexion_agent(self, nom_utilisateur: str, mdp_sale_hashe: str) -> dict:
        curseur = DBConnexion().connexion.cursor()
        curseur.execute("SELECT * FROM agents WHERE nom_utilisateur=:login AND mot_de_passe=:pwd",
                        {"login": nom_utilisateur, "pwd": mdp_sale_hashe})
        row = curseur.fetchone()
        curseur.close()
        if row is not None:
            data = dict(zip(row.keys(), row))
            data = self.__sqlite_to_dao(data)
        else:
            data = None
        return data

    def modifier_identifiants(self, id_agent: int, nom_utilisateur: str, mdp_sale_hashe: str) -> bool:
        try:
            curseur = DBConnexion().connexion.cursor()
            curseur.execute("""
            UPDATE agents SET nom_utilisateur=:login, mot_de_passe=:pwd
            WHERE identifiant_agent=:id
            """, {'id': id_agent, 'login': nom_utilisateur, 'pwd': mdp_sale_hashe})
            DBConnexion().connexion.commit()
            curseur.close()
            return True
        except Exception as e:
            print(e)
            return False

    def verifier_identifiants(self, id_agent: int, nom_utilisateur: str, mdp_sale_hashe: str) -> bool:
        curseur = DBConnexion().connexion.cursor()
        curseur.execute("SELECT nom_utilisateur, mot_de_passe FROM agents WHERE identifiant_agent=:id",
                        {'id': id_agent})
        row = curseur.fetchone()
        curseur.close()
        return nom_utilisateur == row['nom_utilisateur'] and mdp_sale_hashe == row['mot_de_passe']

    def recuperer_nom_utilisateur(self, id_agent: int) -> str:
        curseur = DBConnexion().connexion.cursor()
        curseur.execute("SELECT nom_utilisateur FROM agents WHERE identifiant_agent=:id", {"id": id_agent})
        row = curseur.fetchone()
        curseur.close()
        data = str(row['nom_utilisateur'])
        return data

    def recuperer_dernier_id_agent(self) -> int:
        curseur = DBConnexion().connexion.cursor()
        curseur.execute("SELECT seq FROM sqlite_sequence WHERE name='agents'")
        row = curseur.fetchone()
        curseur.close()
        value = row["seq"]
        return value

    def recuperer_id_superviseur(self, id_agent: int) -> int:
        curseur = DBConnexion().connexion.cursor()
        curseur.execute("SELECT identifiant_superviseur FROM agents WHERE identifiant_agent=:id", {"id": id_agent})
        row = curseur.fetchone()
        curseur.close()
        data = int(row['identifiant_superviseur'])
        return data
