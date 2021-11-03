from typing import Tuple
from typing import List
from BusinessLayer.BusinessObjects.agent import Agent
from BusinessLayer.BusinessObjects.session import Session
from DataLayer.DAO.db_connexion import DBConnexion
from DataLayer.DAO.interface_agent import InterfaceAgent
from hashlib import sha512

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
        
    def deleguer_equipe_a(self, session_utilisateur : Session, id_superviseur : int) -> bool:
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

    def creer_agent(self, est_superviseur : bool, quotite : float, id_superviseur : int, nom_utilisateur : str, mot_de_passe : str, prenom : str, nom : str) -> bool:
        try:
            curseur = DBConnexion().connexion.cursor()
            curseur.execute("""
            INSERT INTO agents (est_superviseur, quotite, identifiant_superviseur, nom_utilisateur, mot_de_passe, prenom, nom)
            VALUES(:est_sup, :quot, :id_sup, :nom_ut, :mdp, :prenom, :nom)
            """, {"est_sup" : est_superviseur, "quot" : quotite, "id_sup" : id_superviseur, "nom_ut" : nom_utilisateur, "mdp" : sha512(nom_utilisateur + mot_de_passe), "prenom" : prenom, "nom" : nom})
            DBConnexion().connexion.commit()
            curseur.close()
            return True
        except Exception as e:
            print(e)
            return False

    def modifier_agent(self, agent_a_modifier : Agent, data : dict) -> bool:
        data["id_agent"] = str(agent_a_modifier.agent_id)
        data["mot_de_passe"] = str(sha512(data["nom_utilisateur"] + data["mot_de_passe"]))
        try:
            curseur = DBConnexion().connexion.cursor()
            curseur.execute("""
            UPDATE agents SET est_superviseur=:est_sup, quotite=:quot, identifiant_superviseur=:id_sup, 
            nom_utilisateur=:nom_ut, mot_de_passe=:mdp, prenom=:prenom, nom=:nom)
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

    def verifier_si_superviseur(self, id_agent : int) -> bool:
        curseur = DBConnexion().connexion.cursor()
        curseur.execute("SELECT est_superviseur FROM agents WHERE identitfiant_agent=: id", {"id": id_agent})
        rows = curseur.fetchall()
        curseur.close()
        answer = list()
        for row in rows:
            data = dict(zip(row.keys(), row))
            data = self.__sqlite_to_dao(data)
            answer.append(data)
        return answer

    def recuperer_mdp_agent(self, nom_utilisateur : str) -> str:
        curseur = DBConnexion().connexion.cursor()
        curseur.execute("SELECT mot_de_passe FROM agents WHERE nom_utilisateur=: utilisateur", {"utilisateur": nom_utilisateur})
        rows = curseur.fetchall()
        curseur.close()
        answer = list()
        for row in rows:
            data = dict(zip(row.keys(), row))
            data = self.__sqlite_to_dao(data)
            answer.append(data)
        return answer
    
    def recuperer_agent_id(self, nom_utilisateur : str) -> int:
        curseur = DBConnexion().connexion.cursor()
        curseur.execute("SELECT identifiant_agent FROM agents WHERE nom_utilisateur=: utilisateur", {"utilisateur": nom_utilisateur})
        rows = curseur.fetchall()
        curseur.close()
        answer = list()
        for row in rows:
            data = dict(zip(row.keys(), row))
            data = self.__sqlite_to_dao(data)
            answer.append(data)
        return answer

    def recuperer_agent_identite(self, nom_utilisateur : str) -> Tuple:
        curseur = DBConnexion().connexion.cursor()
        curseur.execute("SELECT prenom, nom FROM agents WHERE nom_utilisateur=: utilisateur", {"utilisateur": nom_utilisateur})
        rows = curseur.fetchall()
        curseur.close()
        answer = list()
        for row in rows:
            data = dict(zip(row.keys(), row))
            data = self.__sqlite_to_dao(data)
            answer.append(data)
        return answer

    def recuperer_superviseur_id(self, nom_utilisateur : str) -> int:
        curseur = DBConnexion().connexion.cursor()
        curseur.execute("SELECT identifiant_superviseur FROM agents WHERE nom_utilisateur=: utilisateur", {"utilisateur": nom_utilisateur})
        rows = curseur.fetchall()
        curseur.close()
        answer = list()
        for row in rows:
            data  = dict(zip(row.keys(), row))
            data = self.__sqlite_to_dao(data)
            answer.append(data)
        return answer