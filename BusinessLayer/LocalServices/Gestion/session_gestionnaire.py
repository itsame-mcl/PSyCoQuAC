from BusinessLayer.LocalServices.Gestion.interface_session import InterfaceSession
from BusinessLayer.BusinessObjects.gestionnaire import Gestionnaire
from DataLayer import DAO as dao
from BusinessLayer.BusinessObjects.session import Session

class SessionGestionnaire(InterfaceSession):
    
    def ouvrir_session(self, nom_utilisateur, mot_de_passe):
        print("Ouverture de la session")
        agent_id = dao.recuperer_agent_id(nom_utilisateur)
        identite = dao.recuperer_agent_identite(nom_utilisateur)
        superviseur_id = dao.recuperer_superviseur_id(nom_utilisateur)
        return Session(Gestionnaire(agent_id, nom_utilisateur, identite, superviseur_id), False)

    def fermer_session(self):
        del self
        print("Fermeture de la session")