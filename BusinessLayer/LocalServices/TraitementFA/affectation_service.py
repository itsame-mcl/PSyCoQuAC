from random import *
from typing import Dict, List
from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
from DataLayer.DAO.dao_agent import DAOAgent
from utils.singleton import Singleton


class AffectationService(metaclass=Singleton):

    @staticmethod
    def proposer_repartition(id_lot: int, id_agents: List[int],
                             poids_controle: float = 0.01, poids_reprise: float = 0.01):
        # Calcul de la capacité de travail de chaque agent et de l'ensemble de l'équipe sélectionnée
        charge_par_agent = {}
        proposition_de_repartition = {}
        charge_actuelle_totale = 0
        quotite_totale = 0
        for agent in id_agents:
            charge_de_l_agent = {}
            controle = DAOFicheAdresse().obtenir_statistiques(filtre_pot=agent, filtre_code_resultat="TC")[0][0]
            reprise = DAOFicheAdresse().obtenir_statistiques(filtre_pot=agent, filtre_code_resultat="TR")[0][0]
            charge_de_l_agent['actuelle'] = controle * poids_controle + reprise * poids_reprise
            charge_actuelle_totale += charge_de_l_agent['actuelle']
            charge_de_l_agent['quotite'] = DAOAgent().recuperer_quotite(agent)
            quotite_totale += charge_de_l_agent['quotite']
            charge_par_agent[str(agent)] = charge_de_l_agent
            proposition_de_repartition[str(agent)] = {'reprise': 0, 'controle': 0}
        # Calcul de la charge de travail représentée par le lot
        controle_lot = DAOFicheAdresse().obtenir_statistiques(filtre_lot=id_lot, filtre_code_resultat="TH")[0][0]
        charge_controle_lot = controle_lot * poids_controle
        reprise_lot = DAOFicheAdresse().obtenir_statistiques(filtre_lot=id_lot, filtre_code_resultat="TR")[0][0]
        charge_reprise_lot = reprise_lot * poids_reprise
        # Elaboration de la proposition de répartition
        if reprise_lot > 0:
            base_quotite = quotite_totale
            base_charge = charge_actuelle_totale + charge_reprise_lot
            # On commence par répartir le travail obligatoire de reprise en proportion de la quotité des agents
            for agent in id_agents:
                part_quotite = charge_par_agent[str(agent)]['quotite'] / base_quotite
                part_charge = part_quotite * base_charge
                if part_charge >= charge_par_agent[str(agent)]['actuelle']:
                    nouvelle_charge = part_charge - charge_par_agent[str(agent)]['actuelle']
                    base_charge -= part_charge
                    proposition_de_repartition[str(agent)]['reprise'] = round(nouvelle_charge/poids_reprise)
                else:
                    # Si un agent est déjà très surchargé, on ne lui affecte pas de nouvelle charge
                    base_charge -= charge_par_agent[str(agent)]['actuelle']
                base_quotite -= charge_par_agent[str(agent)]['quotite']
        if controle_lot > 0:
            # Si des fiches sont éligibles au contrôle
            quotite_restante = 0
            for agent in id_agents:
                quotite_restante += max(charge_par_agent[str(agent)]['quotite'] - \
                                    charge_par_agent[str(agent)]['actuelle'] - \
                                    proposition_de_repartition[str(agent)]['reprise'] * poids_reprise, 0)
            if quotite_restante > 0:
                # Et si il reste de la charge disponible après affectation des fiches en reprise
                fiches_controlables = round(quotite_restante/poids_controle)
                if controle_lot > fiches_controlables:
                    # Si il y'a plus de fiches à contrôler que de fiches contrôlables, on sature les quotités
                    for agent in id_agents:
                        capacite_restante = charge_par_agent[str(agent)]['quotite'] -\
                                            charge_par_agent[str(agent)]['actuelle'] -\
                                            proposition_de_repartition[str(agent)]['reprise'] * poids_reprise
                        fiches_a_controler = round(capacite_restante/poids_controle)
                        if fiches_a_controler > 0:
                            proposition_de_repartition[str(agent)]['controle'] = fiches_a_controler
                else:
                    # Si toutes les fiches peuvent être contrôlées, on répartit selon la quotité
                    base_quotite = quotite_totale
                    base_charge = charge_actuelle_totale + charge_reprise_lot + charge_controle_lot
                    for agent in id_agents:
                        part_quotite = charge_par_agent[str(agent)]['quotite'] / base_quotite
                        part_charge = part_quotite * base_charge
                        if part_charge >= (charge_par_agent[str(agent)]['actuelle'] +
                                           proposition_de_repartition[str(agent)]['reprise'] * poids_reprise):
                            nouvelle_charge = part_charge - charge_par_agent[str(agent)]['actuelle'] -\
                                              proposition_de_repartition[str(agent)]['reprise'] * poids_reprise
                            base_charge -= part_charge
                            proposition_de_repartition[str(agent)]['controle'] = round(nouvelle_charge / poids_controle)
                        else:
                            # Si un agent est déjà très surchargé, on ne lui affecte pas de nouvelle charge
                            base_charge -= charge_par_agent[str(agent)]['actuelle'] +\
                                           proposition_de_repartition[str(agent)]['reprise'] * poids_reprise
                        base_quotite -= charge_par_agent[str(agent)]['quotite']
        # A la fin du calcul, on retourne la répartition proposée
        return proposition_de_repartition

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
