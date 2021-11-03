from BusinessLayer.LocalServices.Gestion.interface_session import InterfaceSession
from BusinessLayer.BusinessObjects.superviseur import Superviseur
from DataLayer import DAO as dao
from BusinessLayer.BusinessObjects.session import Session

class SessionSuperviseur(InterfaceSession):
    
    def ouvrir_session(self, nom_utilisateur, mot_de_passe):
        print("Ouverture de la session")
        agent_id = dao.DAOAgent.recuperer_agent_id(nom_utilisateur)
        identite = dao.DAOAgent.recuperer_agent_identite(nom_utilisateur)
        superviseur_id = dao.DAOAgent.recuperer_superviseur_id(nom_utilisateur)
        return Session(Superviseur(agent_id, nom_utilisateur, identite), True)

    def fermer_session(self):
        del self
        print("Fermeture de la session")