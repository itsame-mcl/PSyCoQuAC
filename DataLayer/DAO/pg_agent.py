from typing import List
from DataLayer.DAO.db_connexion import DBConnexion
from DataLayer.DAO.interface_agent import InterfaceAgent


class PGAgent(InterfaceAgent):
    def recuperer_agent(self, id_agent: int) -> dict:
        with DBConnexion().connexion.cursor() as curseur:
            row = curseur.execute("SELECT * FROM agents WHERE identifiant_agent=(%s)", (id_agent,)).fetchone()
        return row

    def recuperer_liste_agents(self, id_superviseur: int, agents_delegues: bool = False) -> List[dict]:
        if id_superviseur > 0:
            params = (id_superviseur,)
            if not agents_delegues:
                request = "SELECT * FROM agents WHERE identifiant_superviseur =(%s)"
            else:
                request = """SELECT * FROM agents
                WHERE identifiant_superviseur =(%s) AND identifiant_delegue IS NOT NULL"""
        else:
            params = ()
            request = "SELECT * FROM agents"
        with DBConnexion().connexion.cursor() as curseur:
            rows = curseur.execute(request, params).fetchall()
        return rows

    def supprimer_agent(self, id_agent: int) -> bool:
        try:
            with DBConnexion().connexion.cursor() as curseur:
                curseur.execute("DELETE FROM agents WHERE identifiant_agent=(%s)", (id_agent,))
            return True
        except Exception as e:
            print(e)
            return False

    def creer_agent(self, data: dict) -> bool:
        try:
            with DBConnexion().connexion.cursor() as curseur:
                curseur.execute("""
                INSERT INTO agents (est_superviseur, quotite, identifiant_superviseur,
                nom_utilisateur, mot_de_passe, prenom, nom)
                VALUES((%s), (%s), (%s), (%s), (%s), (%s), (%s))
                """, (data['est_superviseur'], data['quotite'], data['identifiant_superviseur'],
                      data['nom_utilisateur'], data['mot_de_passe'], data['prenom'], data['nom']))
            return True
        except Exception as e:
            print(e)
            return False

    def modifier_agent(self, data: dict) -> bool:
        try:
            with DBConnexion().connexion.cursor() as curseur:
                curseur.execute("""
                UPDATE agents SET est_superviseur=(%s), quotite=(%s),
                identifiant_superviseur=(%s), prenom=(%s), nom=(%s)
                WHERE identifiant_agent=(%s)
                """, (data['est_superviseur'], data['quotite'], data['identifiant_superviseur'],
                      data['prenom'], data['nom'], data['identifiant_agent']))
            return True
        except Exception as e:
            print(e)
            return False

    def deleguer_agent(self, id_agent: int, id_superviseur_delegue: int) -> bool:
        try:
            with DBConnexion().connexion.cursor() as curseur:
                row = curseur.execute("""SELECT identifiant_superviseur FROM agents
                WHERE identifiant_agent=(%s)""", (id_agent,)).fetchone()
                superviseur_actuel = row['identifiant_superviseur']
                curseur.execute("""
                UPDATE agents SET 
                identifiant_superviseur=(%s), identifiant_delegue=(%s)
                WHERE identifiant_agent=(%s)
                """, (id_superviseur_delegue, superviseur_actuel, id_agent))
            return True
        except Exception as e:
            print(e)
            return False

    def retroceder_agent(self, id_agent: int) -> bool:
        try:
            with DBConnexion().connexion.cursor() as curseur:
                row = curseur.execute("""SELECT identifiant_delegue FROM agents
                WHERE identifiant_agent=(%s)""", (id_agent,)).fetchone()
                superviseur_historique = row['identifiant_delegue']
                curseur.execute("""
                UPDATE agents SET 
                identifiant_superviseur=(%s), identifiant_delegue = NULL
                WHERE identifiant_agent=(%s)
                """, (superviseur_historique, id_agent))
            return True
        except Exception as e:
            print(e)
            return False

    def transferer_agent(self, id_agent, id_nouveau_superviseur: int) -> bool:
        try:
            with DBConnexion().connexion.cursor() as curseur:
                curseur.execute("""
                UPDATE agents SET identifiant_superviseur=(%s) WHERE identifiant_agent=(%s)
                """, (id_nouveau_superviseur, id_agent))
            return True
        except Exception as e:
            print(e)
            return False

    def promouvoir_agent(self, agent_a_promouvoir: int) -> bool:
        try:
            with DBConnexion().connexion.cursor() as curseur:
                curseur.execute("""
                UPDATE agents SET est_superviseur=true, identifiant_superviseur=(%s) WHERE identifiant_agent=(%s)
                """, (agent_a_promouvoir, agent_a_promouvoir))
            return True
        except Exception as e:
            print(e)
            return False

    def connexion_agent(self, nom_utilisateur: str, mdp_sale_hashe: str) -> dict:
        with DBConnexion().connexion.cursor() as curseur:
            row = curseur.execute("SELECT * FROM agents WHERE nom_utilisateur=(%s) AND mot_de_passe=(%s)",
                                  (nom_utilisateur, mdp_sale_hashe)).fetchone()
        return row

    def modifier_identifiants(self, id_agent: int, nom_utilisateur: str, mdp_sale_hashe: str) -> bool:
        try:
            with DBConnexion().connexion.cursor() as curseur:
                curseur.execute("""
                UPDATE agents SET nom_utilisateur=(%s), mot_de_passe=(%s)
                WHERE identifiant_agent=(%s)
                """, (nom_utilisateur, mdp_sale_hashe, id_agent))
            return True
        except Exception as e:
            print(e)
            return False

    def verifier_identifiants(self, id_agent: int, nom_utilisateur: str, mdp_sale_hashe: str) -> bool:
        with DBConnexion().connexion.cursor() as curseur:
            row = curseur.execute("SELECT nom_utilisateur, mot_de_passe FROM agents WHERE identifiant_agent=(%s)",
                                  (id_agent,)).fetchone()
        return nom_utilisateur == row['nom_utilisateur'] and mdp_sale_hashe == row['mot_de_passe']

    def recuperer_quotite(self, id_agent: int) -> float:
        with DBConnexion().connexion.cursor() as curseur:
            row = curseur.execute("SELECT quotite FROM agents WHERE identifiant_agent=(%s)", (id_agent,)).fetchone()
        data = row['quotite']
        return data

    def recuperer_nom_utilisateur(self, id_agent: int) -> str:
        with DBConnexion().connexion.cursor() as curseur:
            row = curseur.execute("SELECT nom_utilisateur FROM agents WHERE identifiant_agent=(%s)",
                                  (id_agent,)).fetchone()
        curseur.close()
        data = row['nom_utilisateur']
        return data

    def recuperer_dernier_id_agent(self) -> int:
        with DBConnexion().connexion.cursor() as curseur:
            row = curseur.execute("SELECT last_value, is_called FROM agents_identifiant_agent_seq").fetchone()
        if row["is_called"]:
            value = row["last_value"]
        else:
            value = row["last_value"] - 1
        return value

    def recuperer_id_superviseur(self, id_agent: int) -> int:
        with DBConnexion().connexion.cursor() as curseur:
            row = curseur.execute("SELECT identifiant_superviseur FROM agents WHERE identifiant_agent=(%s)",
                                  (id_agent,)).fetchone()
        data = row['identifiant_superviseur']
        return data
