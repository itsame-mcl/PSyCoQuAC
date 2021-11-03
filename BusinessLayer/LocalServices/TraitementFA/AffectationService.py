from random import *
from typing import Dict, List

from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from BusinessLayer.BusinessObjects.session import Session
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
from DataLayer.DAO.interface_agent import InterfaceAgent

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
            raise ValueError("Le gestionnaire ne peut pas appliquer la répartition des fiches")
        for agent in repartition.items() :
            res = DAOFicheAdresse.affecter_fiches_adresse(agent, repartition[agent]) #On affecte les fiches
        return True
        