from secrets import choice
from math import floor
from typing import Dict, List, Tuple
from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
from DataLayer.DAO.dao_agent import DAOAgent
from utils.singleton import Singleton
from utils.progress_bar import printProgressBar


class AffectationService(metaclass=Singleton):
    PROGRESSION = 'Progression :'
    TERMINE = 'terminé'

    @staticmethod
    def __repartir_selon_quotites(valeur_cible: int, repartition: dict, charge: dict,
                                  type_fiche: str, poids_reprise: float, poids_controle: float) -> dict:
        """
        Cette méthode permet de répartir les fiches adresse à contrôler/reprendre entre les agents,
        en fonction de la quotité de travail et du pot de ces derniers.

        :param valeur_cible: nombre de fiches à répartir
        :param repartition: état actuel de la proposition de répartition
        :param charge: information sur la charge actuelle/totale des agents
        :param type_fiche: type de fiches à répartir
        :param poids_reprise: poids de charge d'une fiche à reprendre
        :param poids_controle: poids de charge d'une fiche à contrôler
        :return: proposition de répartition intégrant les fiches à répartir de manière équitable
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
        Cette méthode permet de corriger les erreurs d'arrondis pouvant survenir lors de la répartition
        proportionnelle.
        :param valeur_cible: nombre correct de fiches à avoir dans la répartition
        :param repartition: état actuel de la répartition
        :param type_fiche: type de fiches dont la répartition est à corriger
        :return: version corrigée des erreurs d'arrondis de la proposition de répartition
        """
        valeur_affectee = sum([repart_agent[type_fiche] for repart_agent in repartition.values()])
        difference = valeur_cible - valeur_affectee
        while difference != 0:
            if difference > 0:
                # Si des fiches sont encore à affecter en raison des arrondis, on charge à partir de la fin
                agents_a_charger = list(repartition.keys())[-difference:]
                for agent in agents_a_charger:
                    repartition[agent][type_fiche] += 1
                    difference -= 1
            elif difference < 0:
                # Si des fiches ont été affectées en trop, on décharge à partir du début
                agents_a_decharger = list(repartition.keys())[:-difference]
                for agent in agents_a_decharger:
                    repartition[agent][type_fiche] -= 1
                    difference += 1
        return repartition

    @staticmethod
    def __saturer_quotites(repartition: dict, charge: dict, type_fiche: str,
                           poids_reprise: float, poids_controle: float):
        if type_fiche == 'reprise':
            poids_cible = poids_reprise
        elif type_fiche == 'controle':
            poids_cible = poids_controle
        else:
            raise ValueError
        for agent in list(repartition.keys()):
            capacite_restante = charge[str(agent)]['quotite'] - charge[str(agent)]['actuelle'] - \
                                repartition[str(agent)]['reprise'] * poids_reprise - \
                                repartition[str(agent)]['controle'] * poids_controle
            fiches_a_ajouter = floor(capacite_restante / poids_cible)  # floor permet de ne pas dépasser la quotité
            if fiches_a_ajouter > 0:
                repartition[str(agent)][type_fiche] = fiches_a_ajouter
        return repartition

    @staticmethod
    def obtenir_charge_actuelle(id_agents: List[int], poids_reprise: float = 0.01,
                                poids_controle: float = 0.01) -> dict:
        charge_actuelle = {str(agent): {'actuelle': 0.0, 'quotite': 0.0} for agent in id_agents}
        # Récupération des informations sur la charge actuelle et la quotité des agents sélectionnés
        for agent in id_agents:
            reprise = DAOFicheAdresse().obtenir_statistiques(filtre_pot=agent, filtre_code_resultat="TR")[0][0]
            controle = DAOFicheAdresse().obtenir_statistiques(filtre_pot=agent, filtre_code_resultat="TC")[0][0]
            charge_actuelle[str(agent)]['actuelle'] = round(reprise * poids_reprise + controle * poids_controle, 5)
            charge_actuelle[str(agent)]['quotite'] = DAOAgent().recuperer_quotite(agent)
        return charge_actuelle

    def proposer_repartition(self, id_lot: int, id_agents: List[int],
                             poids_reprise: float = 0.01, poids_controle: float = 0.01):
        """
        Cette méthode permet de proposer une répartition des fiches adresse à contrôler/à reprendre
        entre une liste d'agents dont on renseigne les identifiants de la base de données Agents.

        :param id_lot: identifiant du lot sur lequel proposer la répartition
        l'identifiant de lot, dans la base de données FA, des fiches adresse à répartir
        :param id_agents:
        la liste des identifiants, dans la base de données Agents, des agents entre
        lesquels la répartition des fiches adresse est effectuée
        :param poids_controle: poids, en points de quotité, d'une fiche en contrôle
        :param poids_reprise: poids, en points de quotité, d'une fiche en reprise
        :return: proposition de répartition équitable
        """
        proposition_de_repartition = {str(agent): {'reprise': 0, 'controle': 0} for agent in id_agents}
        charge_par_agent = self.obtenir_charge_actuelle(id_agents, poids_reprise, poids_controle)
        # Calcul de la charge de travail représentée par le lot
        reprise_lot = DAOFicheAdresse().obtenir_statistiques(filtre_lot=id_lot, filtre_code_resultat="TR")[0][0]
        controle_lot = DAOFicheAdresse().obtenir_statistiques(filtre_lot=id_lot, filtre_code_resultat="TH")[0][0]
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
                    proposition_de_repartition = self.__saturer_quotites(proposition_de_repartition,
                                                                         charge_par_agent, 'controle',
                                                                         poids_reprise, poids_controle)
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
        Tire un échantillon aléatoire de fiches, marque celles tirées comme étant à contrôler et valide les autres
        :param lot_fiches: liste de fiches servant de base d'échantilonnage
        :param taille_echantillon: taille de l'échantillon à tirer
        :return: un tuple composé d'une première liste de fiches échantillonnées, puis d'une liste de fiches validées
        """
        base_tirage = lot_fiches[:]
        echantillon_tc = []
        for _ in range(taille_echantillon):
            selected = choice(base_tirage)
            echantillon_tc.append(selected)
            base_tirage.remove(selected)
        for fiche in lot_fiches:
            if fiche in echantillon_tc:
                fiche.code_res = "TC"
            else:
                fiche.code_res = "VA"
        return [fiche for fiche in lot_fiches if fiche.code_res == "TC"], \
               [fiche for fiche in lot_fiches if fiche.code_res == "VA"]

    def appliquer_repartition(self, id_lot: int, repartition: Dict, verbose: bool = False) -> bool:
        """
        Applique une répartition de fiches à un lot
        :param id_lot: lot sur lequel appliquer la répartition
        :param repartition: informations de répartition des fiches entre les agents
        :param verbose: indique si l'opération doit produire un affichage écran
        :return: un boolean à True si l'opération s'est bien passée et à False sinon
        """
        lot = DAOFicheAdresse().recuperer_lot(id_lot)
        taille_echantillon_controle = sum([item['controle'] for item in repartition.values()])
        lot_a_echantillonner = [fiche for fiche in lot if fiche.code_res == "TH"]
        lot_tc, lot_va = self.echantilloner_fiches(lot_a_echantillonner, taille_echantillon_controle)
        lot_tr = [fiche for fiche in lot if fiche.code_res == "TR"]
        res = True
        progression = 0
        if verbose:
            printProgressBar(progression, len(lot), prefix=self.PROGRESSION, suffix=self.TERMINE, length=50)
        for id_agent, repartition_agent in repartition.items():
            fiches_agent_reprise = lot_tr[:repartition_agent['reprise']]
            if len(fiches_agent_reprise) > 0:
                ids_reprise = [fiche.fiche_id for fiche in fiches_agent_reprise]
                update = DAOFicheAdresse().affecter_fiches_adresse(id_agent, "TR", ids_reprise)
                res = res * update
                if verbose and update:
                    progression += len(ids_reprise)
                    printProgressBar(progression, len(lot), prefix=self.PROGRESSION, suffix=self.TERMINE, length=50)
            fiches_agent_controle = (lot_tc[:repartition_agent['controle']])
            if len(fiches_agent_controle) > 0:
                ids_controle = [fiche.fiche_id for fiche in fiches_agent_controle]
                update = DAOFicheAdresse().affecter_fiches_adresse(id_agent, "TC", ids_controle)
                res = res * update
                if verbose and update:
                    progression += len(ids_controle)
                    printProgressBar(progression, len(lot), prefix=self.PROGRESSION, suffix=self.TERMINE, length=50)
            lot_tr = lot_tr[repartition_agent['reprise']:]
            lot_tc = lot_tc[repartition_agent['controle']:]
        if len(lot_va) > 0:
            id_superviseur = lot_va[0].agent_id * -1
            ids_va = [fiche.fiche_id for fiche in lot_va]
            update = DAOFicheAdresse().affecter_fiches_adresse(id_superviseur, "VA", ids_va)
            res = res * update
            if verbose:
                progression += len(ids_va)
                printProgressBar(progression, len(lot), prefix=self.PROGRESSION, suffix=self.TERMINE, length=50)
        return res

    @staticmethod
    def lots_a_affecter(id_superviseur: int):
        """
        Retourne la liste des lots à affecter pour un superviseur donné.
        :param id_superviseur:
        l'identifiant, dans la base de données Agents, du superviseur dont on souhaite connaître
        la liste de lots à affecter
        :return:
        renvoie la liste des lots du superviseur étant à affecter
        """
        lots = list()
        res = DAOFicheAdresse().obtenir_statistiques(par_lot=True, filtre_pot=-id_superviseur)
        for ligne in res:
            lots.append(ligne[0])
        rem = DAOFicheAdresse().obtenir_statistiques(par_lot=True, filtre_pot=-id_superviseur,
                                                     filtre_code_resultat="TA")
        for ligne in rem:
            lots.remove(ligne[0])
        return lots
