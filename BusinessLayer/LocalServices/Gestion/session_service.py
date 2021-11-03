from BusinessLayer.LocalServices.Gestion.session_superviseur import SessionSuperviseur
from BusinessLayer.LocalServices.Gestion.session_gestionnaire import SessionGestionnaire
from utils.singleton import Singleton
import DataLayer.DAO as dao
from hashlib import sha512
from tkinter import *
import not_utils

@Singleton
class SessionServices:

    def ouvrir_session(self, nom_utilisateur, mot_de_passe):
        hache = sha512(nom_utilisateur + mot_de_passe)
        mdp = dao.DAOAgent.recuperer_mdp_agent(nom_utilisateur)
        if hache == mdp:
            if dao.DAOAgent.est_superviseur(nom_utilisateur): # la méthode regarder_si_superviseur renvoie True si l'Agent est un superviseur
                self.__interface = SessionSuperviseur()
            else: # l'Agent est un gestionnaire
                self.__interface = SessionGestionnaire()
            self.__connexion = self.__interface.ouvrir_session(nom_utilisateur, mot_de_passe)
        else:
            print("Ah ah ah... Vous n'avez pas dis le mot magique !")
            not_utils.execution(not_utils.Jurassic_Park_GIF.gif, 6)
    
    @property
    def ouverture_session(self):
        

    def fermer_session(self):
        self.__interface.fermer_session