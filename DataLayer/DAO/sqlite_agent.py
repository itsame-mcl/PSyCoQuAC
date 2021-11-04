from typing import List
from BusinessLayer.BusinessObjects.agent import Agent
from DataLayer.DAO.db_connexion import DBConnexion
from DataLayer.DAO.interface_agent import InterfaceAgent


class SQLiteAgent(InterfaceAgent):
    def __sqlite_to_dao(self, data: dict) -> dict:
        data["est_superviseur"] = bool(data["est_superviseur"])
        return data

    def __dao_to_sqlite(self, data: dict):
        data["est_superviseur"] = int(data["est_superviseur"])
        return data

    def deleguer_agent_a(self, id_agents : List[int], id_superviseur : int) -> bool:
        request = "UPDATE agents SET identifiant_superviseur=:id_superviseur WHERE identifiant_agent IN ({})".format(','.join(':{}'.format(i) for i in range(len(id_agents))))
        params = {"id_superviseur": id_superviseur}
        params.update({str(i): id for i, id in enumerate(id_agents)})
        try:
            curseur = DBConnexion().connexion.cursor()
            curseur.execute(request, params)
            DBConnexion().connexion.commit()
            curseur.close()
            return True
        except Exception as e:
            print(e)
            return False
        
    def deleguer_equipe_a(self, id_superviseur : int) -> bool:
        agents = SQLiteAgent.recuperer_liste_agents(id_superviseur)
        id_agents = []
        for agent in agents:
            id_agents.append(agent.agent_id)
        return SQLiteAgent.deleguer_agent_a(id_agents, id_superviseur)

    def recuperer_agent(self, id_agent: int) -> dict:
        curseur = DBConnexion().connexion.cursor()
        curseur.execute("SELECT * FROM agents WHERE identifiant_agent=:id", {"id": id_agent})
        row = curseur.fetchone()
        curseur.close()
        data = dict(zip(row.keys(), row))
        data = self.__sqlite_to_dao(data)
        return data

    def recuperer_liste_agents(self, id_superviseur : int) -> List[Agent]:
        if id_superviseur > 0:
            request = "SELECT * FROM agents WHERE identifiant_superviseur =: id_superviseur"
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
            curseur.execute("DELETE FROM agents WHERE identifiant_agent=: id", {"id": id_agent})
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
            identifiant_superviseur=:identifiant_superviseur, 
            prenom=:prenom, nom=:nom
            WHERE identifiant_agent=:id_agent
            """, data)
            DBConnexion().connexion.commit()
            curseur.close()
            return True
        except Exception as e:
            print(e)
            return False

    def changer_droits(self, agent_a_modifier: Agent) -> bool:
        try:
            curseur = DBConnexion().connexion.cursor()
            curseur.execute("UPDATE agents SET est_superviseur=:not(est_superviseur) WHERE identifiant_agent=: id_agent", {"id_agent": agent_a_modifier.agent_id})
            DBConnexion().connexion.commit()
            curseur.close()
            return True
        except Exception as e:
            print(e)
            return False
