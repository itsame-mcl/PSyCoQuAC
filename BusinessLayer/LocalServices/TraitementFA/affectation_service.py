from random import sample
from math import floor
from typing import Dict, List, Tuple
from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
from DataLayer.DAO.dao_agent import DAOAgent
from utils.singleton import Singleton
from utils.progress_bar import printProgressBar


class AffectationService(metaclass=Singleton):
    @staticmethod
    def __repartir_selon_quotites(valeur_cible: int, repartition: dict, charge: dict,
                                  type_fiche: str, poids_reprise: float, poids_controle: float) -> dict:
        """

        :param valeur_cible:
        :param repartition:
        :param charge:
        :param type_fiche:
        :param poids_reprise:
        :param poids_controle:
        :return:
        """
        if type_fiche == 'reprise':
            poids_cible = poids_reprise
        elif type_fiche == 'controle':
            poids_cible = poids_controle
        else:
            raise ValueError
        # On détermine la valeur initiale de la quotité et de la charge déjà affectée
        base_quotite = sum([charge[agent]['quotite'] for agent in list(charge.keys())])
        charge_initiale = sum([charge[agent]['actuelle'] for agent in list(charge.keys())]) + \
                          sum([repartition[agent]['controle'] * poids_controle for agent in list(charge.keys())]) + \
                          sum([repartition[agent]['reprise'] * poids_reprise for agent in list(charge.keys())])
        # Puis, on calcule la charge représentée par le nouveau travail pour obtenir la base de charge totale
        nouvelle_charge = valeur_cible * poids_cible
        base_charge = charge_initiale + nouvelle_charge
        for agent in list(charge.keys()):
            # Pour chaque agent, on cherche à faire en sorte que sa part de la charge totale soit égale à sa part
            # de la quotité totale
            part_quotite = charge[agent]['quotite'] / base_quotite
            part_charge = part_quotite * base_charge
            charge_actuelle = charge[str(agent)]['actuelle'] + repartition[agent]['controle'] * poids_controle + \
                              repartition[agent]['reprise'] * poids_reprise
            if part_charge >= charge_actuelle:
                # Si l'agent est en capacité de recevoir une partie de la charge, on la convertit en affectation
                nouvelle_charge_agent = part_charge - charge_actuelle
                base_charge -= part_charge
                repartition[agent][type_fiche] = round(nouvelle_charge_agent / poids_cible)
            else:
                # Si un agent est déjà très surchargé, on ne lui affecte pas de nouvelle charge
                base_charge -= charge_actuelle
            base_quotite -= charge[agent]['quotite']
        return repartition

    @staticmethod
    def __corriger_arrondis(valeur_cible: int, repartition: dict, type_fiche: str) -> dict:
        """

        :param valeur_cible:
        :param repartition:
        :param type_fiche:
        :return:
        """
        valeur_affectee = sum([repart_agent[type_fiche] for repart_agent in repartition.values()])
        difference = valeur_cible - valeur_affectee
        if difference > 0:
            # Si des fiches sont encore à affecter en raison des arrondis, on charge à partir de la fin
            agents_a_charger = list(repartition.keys())[-difference:]
            for agent in agents_a_charger:
                repartition[agent][type_fiche] += 1
        elif difference < 0:
            # Si des fiches ont été affectées en trop, on décharge à partir du début
            agents_a_decharger = list(repartition.keys())[:difference]
            for agent in agents_a_decharger:
                repartition[agent][type_fiche] -= 1
        return repartition

    def proposer_repartition(self, id_lot: int, id_agents: List[int],
                             poids_controle: float = 0.01, poids_reprise: float = 0.01):
        """

        :param id_lot:
        :param id_agents:
        :param poids_controle:
        :param poids_reprise:
        :return:
        """
        charge_par_agent = {}
        proposition_de_repartition = {}
        # Récupération des informations sur la charge actuelle et la quotité des agents sélectionnés
        for agent in id_agents:
            charge_de_l_agent = {}
            controle = DAOFicheAdresse().obtenir_statistiques(filtre_pot=agent, filtre_code_resultat="TC")[0][0]
            reprise = DAOFicheAdresse().obtenir_statistiques(filtre_pot=agent, filtre_code_resultat="TR")[0][0]
            charge_de_l_agent['actuelle'] = controle * poids_controle + reprise * poids_reprise
            charge_de_l_agent['quotite'] = DAOAgent().recuperer_quotite(agent)
            charge_par_agent[str(agent)] = charge_de_l_agent
            proposition_de_repartition[str(agent)] = {'reprise': 0, 'controle': 0}
        # Calcul de la charge de travail représentée par le lot
        controle_lot = DAOFicheAdresse().obtenir_statistiques(filtre_lot=id_lot, filtre_code_resultat="TH")[0][0]
        reprise_lot = DAOFicheAdresse().obtenir_statistiques(filtre_lot=id_lot, filtre_code_resultat="TR")[0][0]
        # Elaboration de la proposition de répartition
        if reprise_lot > 0:
            # Calcul d'une répartition proportionnelle à la quotité des fiches
            proposition_de_repartition = self.__repartir_selon_quotites(reprise_lot, proposition_de_repartition,
                                                                        charge_par_agent, 'reprise', poids_reprise,
                                                                        poids_controle)
            # Vérification de la bonne affectation de toutes les fiches
            proposition_de_repartition = self.__corriger_arrondis(reprise_lot, proposition_de_repartition, 'reprise')
        if controle_lot > 0:
            # Si des fiches sont éligibles au contrôle, calcul de la quotité restante disponible
            quotite_restante = sum([max(charge_par_agent[str(agent)]['quotite'] -
                                        charge_par_agent[str(agent)]['actuelle'] -
                                        proposition_de_repartition[str(agent)]['reprise'] * poids_reprise, 0)
                                    for agent in id_agents])
            if quotite_restante > 0:
                # Si il reste de la charge disponible après affectation des fiches en reprise
                capacite_controle = round(quotite_restante / poids_controle)
                if controle_lot > capacite_controle:
                    # Si il y'a plus de fiches à contrôler que de fiches contrôlables, on sature les quotités
                    for agent in id_agents:
                        capacite_restante = charge_par_agent[str(agent)]['quotite'] - \
                                            charge_par_agent[str(agent)]['actuelle'] - \
                                            proposition_de_repartition[str(agent)]['reprise'] * poids_reprise
                        fiches_a_controler = floor(
                            capacite_restante / poids_controle)  # floor permet de ne pas dépasser la quotité
                        if fiches_a_controler > 0:
                            proposition_de_repartition[str(agent)]['controle'] = fiches_a_controler
                else:
                    # Si toutes les fiches peuvent être contrôlées, on répartit selon la quotité
                    proposition_de_repartition = self.__repartir_selon_quotites(controle_lot,
                                                                                proposition_de_repartition,
                                                                                charge_par_agent, 'controle',
                                                                                poids_reprise,
                                                                                poids_controle)
                    # Vérification de la bonne affectation de toutes les fiches
                    proposition_de_repartition = self.__corriger_arrondis(controle_lot, proposition_de_repartition,
                                                                          'controle')
        # A la fin du calcul, on retourne la répartition proposée
        return proposition_de_repartition

    @staticmethod
    def echantilloner_fiches(lot_fiches: List[FicheAdresse], taille_echantillon: int) -> \
            Tuple[List[FicheAdresse], List[FicheAdresse]]:
        """

        :param lot_fiches:
        :param taille_echantillon:
        :return:
        """
        echantillon_tc = sample(lot_fiches, taille_echantillon)
        for fiche in lot_fiches:
            if fiche in echantillon_tc:
                fiche.code_res = "TC"
            else:
                fiche.code_res = "VA"
        return [fiche for fiche in lot_fiches if fiche.code_res == "TC"], \
               [fiche for fiche in lot_fiches if fiche.code_res == "VA"]

    def appliquer_repartition(self, id_lot: int, repartition: Dict, verbose: bool = False) -> bool:
        """

        :param id_lot:
        :param repartition:
        :param verbose:
        :return:
        """
        lot = DAOFicheAdresse().recuperer_lot(id_lot)
        taille_echantillon_controle = sum([item['controle'] for item in repartition.values()])
        lot_a_echantillonner = [fiche for fiche in lot if fiche.code_res == "TH"]
        lot_tc, lot_va = self.echantilloner_fiches(lot_a_echantillonner, taille_echantillon_controle)
        lot_tr = [fiche for fiche in lot if fiche.code_res == "TR"]
        res = True
        progression = 0
        if verbose:
            printProgressBar(progression, len(lot), prefix='Progression :', suffix='terminé', length=50)
        for id_agent, repartition_agent in repartition.items():
            fiches_agent = lot_tr[:repartition_agent['reprise']]
            fiches_agent.extend(lot_tc[:repartition_agent['controle']])
            for fiche in fiches_agent:
                fiche.agent_id = int(id_agent)
                update = DAOFicheAdresse().modifier_fiche_adresse(fiche)
                res = res * update
                if verbose:
                    progression += 1
                    printProgressBar(progression, len(lot), prefix='Progression :', suffix='terminé', length=50)
            lot_tr = lot_tr[repartition_agent['reprise']:]
            lot_tc = lot_tc[repartition_agent['controle']:]
        for fiche in lot_va:
            fiche.agent_id = fiche.agent_id * -1
            update = DAOFicheAdresse().modifier_fiche_adresse(fiche)
            res = res * update
            if verbose:
                progression += 1
                printProgressBar(progression, len(lot), prefix='Progression :', suffix='terminé', length=50)
        return res
