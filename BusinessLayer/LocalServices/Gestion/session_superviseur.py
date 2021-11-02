from BusinessLayer.LocalServices.Gestion.interface_session import InterfaceSession
from BusinessLayer.BusinessObjects.Superviseur import Superviseur
from DataLayer import DAO as dao
from BusinessLayer.BusinessObjects.Session import Session

class SessionSuperviseur(InterfaceSession):
    
    def ouvrir_session(self, nom_utilisateur, mot_de_passe):
        print("Ouverture de la session")
        agent_id = dao.recuperer_agent_id(nom_utilisateur)
        identite = dao.recuperer_agent_identite(nom_utilisateur)
        equipe_deleguee_a = dao.recuperer_equipe_deleguee_a(nom_utilisateur)
        return Session(Superviseur(agent_id, nom_utilisateur, identite, equipe_deleguee_a), True)

    def fermer_session(self):
        del self
        print("Fermeture de la session")