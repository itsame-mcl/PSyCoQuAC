from DataLayer.DAO.db_connexion import DBConnexion
from BusinessLayer.BusinessObjects.agent import Agent

class SessionService:

    def ouvrir_session(self, nom_utilisateur, mot_de_passe):
        agent = DBConnexion.connexion(nom_utilisateur, mot_de_passe)
        return agent

    def fermer_session(self):
        raise NotImplemented