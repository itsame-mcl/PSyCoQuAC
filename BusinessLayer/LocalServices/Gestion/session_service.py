from BusinessLayer.LocalServices.Gestion.session_superviseur import SessionSuperviseur
from BusinessLayer.LocalServices.Gestion.session_gestionnaire import SessionGestionnaire
from utils.singleton import Singleton
import DataLayer.DAO as dao
from hashlib import sha512

@Singleton
class SessionServices:

    def ouvrir_session(self, nom_utilisateur, mot_de_passe):
        hache = sha512(nom_utilisateur + mot_de_passe)
        mdp = dao.recuperer_agent_mdp(nom_utilisateur, mot_de_passe)
        if hache == mdp:
            if dao.regarder_si_superviseur(hache): # la méthode regarder_si_superviseur renvoie True si l'Agent est un superviseur
                self.__interface = SessionSuperviseur()
            else: # l'Agent est un gestionnaire
                self.__interface = SessionGestionnaire()
            return self.__connexion = self.__interface.ouvrir_session(nom_utilisateur, mot_de_passe)
        else:
            return "Ah ah ah ! Vous n'avez pas dis le mot magique !"

    def fermer_session(self):
        self.__interface.fermer_session