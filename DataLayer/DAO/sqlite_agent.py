from DataLayer.DAO.db_connexion import DBConnexion
from DataLayer.DAO.interface_agent import InterfaceAgent


class SQLiteAgent(InterfaceAgent):

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
        
    def deleguer_equipe_a(self, session_utilisateur : Session, id_superviseur : int) ->bool:
        agents = SQLiteAgent.recuperer_liste_agents(session_utilisateur.utilisateur_connecte.agent_id)
        id_agents = []
        for agent in agents:
            id_agents.append(agent.agent_id)
        return SQLiteAgent.deleguer_agent_a(id_agents, id_superviseur)

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
            data: dict = dict(zip(row.keys(), row))
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

    def creer_agent(self, session_utilisateur, prenom, nom, nom_utilisateur, mot_de_passe, est_superviseur):
        raise NotImplemented

    def modifier_agent(self, agent_a_modifier):
        data = self.__dao_to_sqlite(data)
        try:
            curseur = DBConnexion().connexion.cursor()
            curseur.execute("""
            UPDATE agents SET identifiant_pot=:identifiant_pot, identifiant_lot=:identifiant_lot,
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

    def changer_droit(self, agent_a_modifier):
        try:
            curseur = DBConnexion().connexion.cursor()
            curseur.execute("UPDATE agents SET est_superviseur=:not(est_superviseur) WHERE identifiant_agent=: id_agent", {"id_agent": agent_a_modifier.agent_id})
            DBConnexion().connexion.commit()
            curseur.close()
            return True
        except Exception as e:
            print(e)
            return False

    def est_superviseur(self, nom_utilisateur):
        try:
            curseur = DBConnexion().connexion.cursor()
            curseur.execute("SELECT est_superviseur FROM agents WHERE nom_utilisateur=: utilisateur", {"utilisateur": nom_utilisateur})
            rows = curseur.fetchall()
            curseur.close()
            answer = list()
            for row in rows:
                data: dict = dict(zip(row.keys(), row))
                data = self.__sqlite_to_dao(data)
                answer.append(data)
            return answer
        except Exception as e:
            print(e)
            return False

    def recuperer_mdp_agent(self, nom_utilisateur):
        try:
            curseur = DBConnexion().connexion.cursor()
            curseur.execute("SELECT mot_de_passe FROM agents WHERE nom_utilisateur=: utilisateur", {"utilisateur": nom_utilisateur})
            rows = curseur.fetchall()
            curseur.close()
            answer = list()
            for row in rows:
                data: dict = dict(zip(row.keys(), row))
                data = self.__sqlite_to_dao(data)
                answer.append(data)
            return answer
        except Exception as e:
            print(e)
            return False