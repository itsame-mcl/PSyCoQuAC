from DataLayer.DAO.dao_agent import DAOAgent
from utils.singleton import Singleton


class SessionService(metaclass=Singleton):
    
    def ouvrir_session(self, nom_utilisateur, mot_de_passe):
        try:
            agent = DAOAgent().connexion_agent(nom_utilisateur, mot_de_passe)
        except ConnectionRefusedError:
            agent = None
        return agent

    def fermer_session(self):
        raise NotImplemented
