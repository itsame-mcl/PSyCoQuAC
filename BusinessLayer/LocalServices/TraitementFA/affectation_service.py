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
                    proposition_de_repartition[str(agent)]['reprise'] = round(nouvelle_charge / poids_reprise)
                else:
                    # Si un agent est déjà très surchargé, on ne lui affecte pas de nouvelle charge
                    base_charge -= charge_par_agent[str(agent)]['actuelle']
                base_quotite -= charge_par_agent[str(agent)]['quotite']
        # Vérification de la bonne affectation de toutes les fiches
        reprise_affectee = sum([repart_agent['reprise'] for repart_agent in proposition_de_repartition.values()])
        diff_reprise = reprise_lot - reprise_affectee
        if diff_reprise > 0:
            # Si des fiches sont encore à affecter en raison des arrondis, on charge à partir de la fin
            agents_a_charger = id_agents[-diff_reprise:]
            for agent in agents_a_charger:
                proposition_de_repartition[str(agent)]['reprise'] += 1
        elif diff_reprise < 0:
            # Si des fiches ont été affectées en trop, on décharge à partir du début
            agents_a_decharger = id_agents[:diff_reprise]
            for agent in agents_a_decharger:
                proposition_de_repartition[str(agent)]['reprise'] -= 1
        if controle_lot > 0:
            # Si des fiches sont éligibles au contrôle
            quotite_restante = 0
            for agent in id_agents:
                quotite_restante += max(charge_par_agent[str(agent)]['quotite'] -
                                        charge_par_agent[str(agent)]['actuelle'] -
                                        proposition_de_repartition[str(agent)]['reprise'] * poids_reprise, 0)
            if quotite_restante > 0:
                # Et si il reste de la charge disponible après affectation des fiches en reprise
                fiches_controlables = round(quotite_restante / poids_controle)
                if controle_lot > fiches_controlables:
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
                    base_quotite = quotite_totale
                    base_charge = charge_actuelle_totale + charge_reprise_lot + charge_controle_lot
                    for agent in id_agents:
                        part_quotite = charge_par_agent[str(agent)]['quotite'] / base_quotite
                        part_charge = part_quotite * base_charge
                        if part_charge >= (charge_par_agent[str(agent)]['actuelle'] +
                                           proposition_de_repartition[str(agent)]['reprise'] * poids_reprise):
                            nouvelle_charge = part_charge - charge_par_agent[str(agent)]['actuelle'] - \
                                              proposition_de_repartition[str(agent)]['reprise'] * poids_reprise
                            base_charge -= part_charge
                            proposition_de_repartition[str(agent)]['controle'] = round(nouvelle_charge / poids_controle)
                        else:
                            # Si un agent est déjà très surchargé, on ne lui affecte pas de nouvelle charge
                            base_charge -= charge_par_agent[str(agent)]['actuelle'] + \
                                           proposition_de_repartition[str(agent)]['reprise'] * poids_reprise
                        base_quotite -= charge_par_agent[str(agent)]['quotite']
                    # Vérification de la bonne affectation de toutes les fiches
                    controle_affecte = sum(
                        [repart_agent['controle'] for repart_agent in proposition_de_repartition.values()])
                    diff_controle = controle_lot - controle_affecte
                    if diff_controle > 0:
                        # Si des fiches sont encore à affecter en raison des arrondis, on charge à partir de la fin
                        agents_a_charger = id_agents[-diff_controle:]
                        for agent in agents_a_charger:
                            proposition_de_repartition[str(agent)]['controle'] += 1
                    elif diff_controle < 0:
                        # Si des fiches ont été affectées en trop, on décharge à partir du début
                        agents_a_decharger = id_agents[:diff_controle]
                        for agent in agents_a_decharger:
                            proposition_de_repartition[str(agent)]['controle'] -= 1
        # A la fin du calcul, on retourne la répartition proposée
        return proposition_de_repartition

    @staticmethod
    def echantilloner_fiches(lot_fiches: List[FicheAdresse], taille_echantillon: int) -> \
            Tuple[List[FicheAdresse], List[FicheAdresse]]:
        echantillon_tc = sample(lot_fiches, taille_echantillon)
        for fiche in lot_fiches:
            if fiche in echantillon_tc:
                fiche.code_res = "TC"
            else:
                fiche.code_res = "VA"
        return [fiche for fiche in lot_fiches if fiche.code_res == "TC"], \
               [fiche for fiche in lot_fiches if fiche.code_res == "VA"]

    def appliquer_repartition(self, id_lot: int, repartition: Dict, verbose:bool = False) -> bool:
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
