from DataLayer.DAO.db_connexion import DBConnexion
from DataLayer.DAO.interface_agent import InterfaceAgent
import DataLayer.DAO.sqlite_fiche_adresse

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

    def recuperer_fiches_agent(self, id_agent : int) -> List[dict]:
        return DataLayer.DAO.sqlite_fiche_adresse.SQLiteFicheAdresse.recuperer_liste_fiches_adresse(id_agent, 0)

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
            curseur.execute("DELETE FROM agents WHERE identifiant_agent=: id_agent", {"id": identifiant})
            DBConnexion().connexion.commit()
            curseur.close()
            return True
        except Exception as e:
            print(e)
            return False