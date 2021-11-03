from random import *
from typing import Dict, List

from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from BusinessLayer.BusinessObjects.session import Session
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
import not_utils

class AffectationService():

    def echantilloner_fiches(fiches_a_controler : List[FicheAdresse], taille_max_travail : int) -> List[FicheAdresse]:
        n = len(fiches_a_controler)
        l = [i for i in range (n)]
        liste_aleatoire = sample(l, taille_max_travail) #Contruction d'une liste aléatoire d'entier compris entre 0 et n-1 de taille nb_fiche_à_controler 
        liste_echantillonne = []
        for i in range (taille_max_travail) :
            liste_echantillonne.append(fiches_a_controler[liste_aleatoire[i]])
        return liste_echantillonne

    def appliquer_repartition(session_utilisateur : Session, repartition : Dict) -> bool :
        if session_utilisateur.droits_superviseurs == False :
            #print("Ah ah ah... Vous n'avez pas dis le mot magique !")
            #not_utils.probleme_droits_agent(not_utils.Jurassic_Park_GIF.gif, 6)
            raise ValueError("Le gestionnaire ne peut pas appliquer la répartition des fiches")
        else:
            for agent in repartition.keys() :
                res = DAOFicheAdresse.affecter_fiches_adresse(agent, repartition[agent]) # On affecte les fiches
            return True       