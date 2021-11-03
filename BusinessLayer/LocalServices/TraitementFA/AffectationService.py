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

    def repartition(session_utilisateur : Session, fiches_a_controler : List[FicheAdresse], taille_max_travail : int, fiches_a_reprendre : List[FicheAdresse]) -> Dict :
        if session_utilisateur.droits_superviseurs == False :
            raise ValueError("Le gestionnaire ne peut pas appliquer la répartition des fiches")
        liste_echantillonne = echantilloner_fiches(fiches_a_controler, taille_max_travail)
        fiches_a_repartir = fiches_a_reprendre + liste_echantillonne
        repartition = {}
        superviseur = session_utilisateur.utilisateur_connecte
        liste_agents = InterfaceAgent.recuperer_liste_agents(superviseur.agent_id)
        for i in range (len(fiches_a_repartir)): #Pour chaque fiche à répartir, on détermine l'agent qui va s'occuper de cette fiche
            fiche_a_repartir = fiches_a_repartir[i]
            id_fiche_a_repartir = fiche_a_repartir.agent_id
            dict_pots = {}
            for agent in liste_agents : #On crée un dictionnaire contenant le nombre de fiches dans le lot de chaque agent
                pot = DAOFicheAdresse.recuperer_pot(agent.agent_id)
                taille_pot = len(pot)
                dict_pots[agent.agent_id] = taille_pot
            min = float("inf")
            agent_choisi = 0
            for (k, val) in dict_pots.items() : #On récupère l'agent qui a le moins de fiches pour lui en ajouter en priorité
                if val < min :
                    min = val
                    agent_choisi = k
            res = DAOFicheAdresse.affecter_fiches_adresse(agent_choisi, [id_fiche_a_repartir]) #On affecte la fiche à l'agent choisi
            repartition[agent_choisi] = id_fiche_a_repartir
        return repartition


    def appliquer_repartition(session_utilisateur : Session, repartition : Dict) -> bool :
        if session_utilisateur.droits_superviseurs == False :
            #print("Ah ah ah... Vous n'avez pas dis le mot magique !")
            #not_utils.probleme_droits_agent(not_utils.Jurassic_Park_GIF.gif, 6)
            raise ValueError("Le gestionnaire ne peut pas appliquer la répartition des fiches")
<<<<<<< HEAD
        for agent in repartition.items() :
            res = DAOFicheAdresse.affecter_fiches_adresse(agent, [repartition[agent]]) #On affecte les fiches
        return True
=======
        else:
            for agent in repartition.keys() :
                res = DAOFicheAdresse.affecter_fiches_adresse(agent, repartition[agent]) # On affecte les fiches
            return True       
>>>>>>> ed5dd14cc7211476f4aaf7b40ede2282ec34842b
