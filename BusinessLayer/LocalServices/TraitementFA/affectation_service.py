from random import *
from typing import Dict, List
from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
from DataLayer.DAO.dao_agent import DAOAgent
from utils.singleton import Singleton


class AffectationService(metaclass=Singleton):
    @staticmethod
    def echantilloner_fiches(fiches_a_controler: List[FicheAdresse], taille_max_travail: int) -> List[FicheAdresse]:
        n = len(fiches_a_controler)
        liste = [i for i in range(n)]
        liste_aleatoire = sample(liste,
                                 taille_max_travail)  # Contruction d'une liste aléatoire d'entier compris entre 0 et
        # n-1 de taille nb_fiche_à_controler
        liste_echantillonne = []
        for i in range(taille_max_travail):
            liste_echantillonne.append(fiches_a_controler[liste_aleatoire[i]])
        return liste_echantillonne

    def repartition(self, id_superviseur: int, fiches_a_controler: List[FicheAdresse], taille_max_travail: int,
                    fiches_a_reprendre: List[FicheAdresse]) -> Dict:
        liste_echantillonne = self.echantilloner_fiches(fiches_a_controler, taille_max_travail)
        fiches_a_repartir = fiches_a_reprendre + liste_echantillonne
        repartition = {}  # repartition est un dictionnaire, avec comme clés les agents_id et comme valeurs les
        # fiches_id
        liste_agents = DAOAgent().recuperer_equipe(id_superviseur)
        for i in range(
                len(fiches_a_repartir)):  # Pour chaque fiche à répartir, on détermine l'agent qui va s'occuper de
            # cette fiche
            fiche_a_repartir = fiches_a_repartir[i]
            id_fiche_a_repartir = fiche_a_repartir.agent_id
            dict_pots = {}
            for agent in liste_agents:  # On crée un dictionnaire contenant le nombre de fiches dans le lot de chaque
                # agent
                pot = DAOFicheAdresse().recuperer_pot(agent.agent_id)
                taille_pot = len(pot)
                dict_pots[agent.agent_id] = taille_pot
            mini = float("inf")
            agent_choisi = 0
            for (k,
                 val) in dict_pots.items():  # On récupère l'agent qui a le moins de fiches pour lui en ajouter en
                # priorité
                if val < mini:
                    mini = val
                    agent_choisi = k
            DAOFicheAdresse().affecter_fiches_adresse(agent_choisi, [
                id_fiche_a_repartir])  # On affecte la fiche à l'agent choisi
            repartition[agent_choisi] = id_fiche_a_repartir
        return repartition

    @staticmethod
    def appliquer_repartition(repartition: Dict) -> bool:
        res = True
        for agent in repartition.keys():
            res_agent = DAOFicheAdresse().affecter_fiches_adresse(agent, repartition[agent])  # On affecte les fiches
            res = res * res_agent
        return res
