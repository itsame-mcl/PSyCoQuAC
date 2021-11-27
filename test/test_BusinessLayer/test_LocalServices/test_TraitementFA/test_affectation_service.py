import os
from random import seed, sample
from unittest import TestCase, mock
from BusinessLayer.BusinessObjects.adresse import Adresse
from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from BusinessLayer.LocalServices.TraitementFA.affectation_service import AffectationService


class TestAffectationService(TestCase):
    def setUp(self):
        self.service = AffectationService()

    def tearDown(self):
        AffectationService.clear()

    def test_repartir_selon_quotite_sans_charge_initiale(self):
        # GIVEN
        valeur_cible = 100
        repartition_2_agents = {'1': {'reprise': 0, 'controle': 0}, '2': {'reprise': 0, 'controle': 0}}
        repartition_3_agents = {'1': {'reprise': 0, 'controle': 0}, '2': {'reprise': 0, 'controle': 0},
                                '3': {'reprise': 0, 'controle': 0}}
        charge_2_agents = {'1': {'actuelle': 0.0, 'quotite': 1.0}, '2': {'actuelle': 0.0, 'quotite': 1.0}}
        charge_3_agents = {'1': {'actuelle': 0.0, 'quotite': 1.0}, '2': {'actuelle': 0.0, 'quotite': 1.0},
                           '3': {'actuelle': 0.0, 'quotite': 1.0}}
        type_fiche = 'reprise'
        poids_reprise = 0.01
        poids_controle = 0.01
        # WHEN
        proposition_2_agents = self.service._AffectationService__repartir_selon_quotites(valeur_cible,
                                                                                         repartition_2_agents,
                                                                                         charge_2_agents, type_fiche,
                                                                                         poids_reprise, poids_controle)
        proposition_3_agents = self.service._AffectationService__repartir_selon_quotites(valeur_cible,
                                                                                         repartition_3_agents,
                                                                                         charge_3_agents, type_fiche,
                                                                                         poids_reprise, poids_controle)
        # THEN
        self.assertEqual({'1': {'reprise': 50, 'controle': 0}, '2': {'reprise': 50, 'controle': 0}},
                         proposition_2_agents)
        self.assertEqual({'1': {'reprise': 33, 'controle': 0}, '2': {'reprise': 33, 'controle': 0},
                         '3': {'reprise': 33, 'controle': 0}}, proposition_3_agents)

    def test_repartir_selon_quotite_avec_charge_initiale(self):
        # GIVEN
        valeur_cible = 125
        repartition_2_agents = {'1': {'reprise': 0, 'controle': 0}, '2': {'reprise': 0, 'controle': 0}}
        repartition_3_agents = {'1': {'reprise': 0, 'controle': 0}, '2': {'reprise': 0, 'controle': 0},
                                '3': {'reprise': 0, 'controle': 0}}
        charge_2_agents = {'1': {'actuelle': 0.25, 'quotite': 1.0}, '2': {'actuelle': 0.5, 'quotite': 1.0}}
        charge_3_agents = {'1': {'actuelle': 0.6666666666666666, 'quotite': 1.0},
                           '2': {'actuelle': 0.5, 'quotite': 1.0},
                           '3': {'actuelle': 0.3333333333333333, 'quotite': 1.0}}
        type_fiche = 'reprise'
        poids_reprise = 0.01
        poids_controle = 0.01
        # WHEN
        proposition_2_agents = self.service._AffectationService__repartir_selon_quotites(valeur_cible,
                                                                                         repartition_2_agents,
                                                                                         charge_2_agents, type_fiche,
                                                                                         poids_reprise, poids_controle)
        proposition_3_agents = self.service._AffectationService__repartir_selon_quotites(valeur_cible,
                                                                                         repartition_3_agents,
                                                                                         charge_3_agents, type_fiche,
                                                                                         poids_reprise, poids_controle)
        # THEN
        self.assertEqual({'1': {'reprise': 75, 'controle': 0}, '2': {'reprise': 50, 'controle': 0}},
                         proposition_2_agents)
        self.assertEqual({'1': {'reprise': 25, 'controle': 0}, '2': {'reprise': 42, 'controle': 0},
                          '3': {'reprise': 58, 'controle': 0}}, proposition_3_agents)

    def test_repartir_selon_quotite_avec_surcharge(self):
        # GIVEN
        valeur_cible = 50
        repartition_2_agents = {'1': {'reprise': 0, 'controle': 0}, '2': {'reprise': 0, 'controle': 0}}
        repartition_3_agents = {'1': {'reprise': 0, 'controle': 0}, '2': {'reprise': 0, 'controle': 0},
                                '3': {'reprise': 0, 'controle': 0}}
        charge_2_agents = {'1': {'actuelle': 1.5, 'quotite': 1.0}, '2': {'actuelle': 0.5, 'quotite': 1.0}}
        charge_3_agents = {'1': {'actuelle': 1.75, 'quotite': 1.0},
                           '2': {'actuelle': 0.6666666666666666, 'quotite': 1.0},
                           '3': {'actuelle': 0.3333333333333333, 'quotite': 1.0}}
        type_fiche = 'reprise'
        poids_reprise = 0.01
        poids_controle = 0.01
        # WHEN
        proposition_2_agents = self.service._AffectationService__repartir_selon_quotites(valeur_cible,
                                                                                         repartition_2_agents,
                                                                                         charge_2_agents, type_fiche,
                                                                                         poids_reprise, poids_controle)
        proposition_3_agents = self.service._AffectationService__repartir_selon_quotites(valeur_cible,
                                                                                         repartition_3_agents,
                                                                                         charge_3_agents, type_fiche,
                                                                                         poids_reprise, poids_controle)
        # THEN
        self.assertEqual({'1': {'reprise': 0, 'controle': 0}, '2': {'reprise': 50, 'controle': 0}},
                         proposition_2_agents)
        self.assertEqual({'1': {'reprise': 0, 'controle': 0}, '2': {'reprise': 8, 'controle': 0},
                          '3': {'reprise': 42, 'controle': 0}}, proposition_3_agents)

    def test_corriger_arrondis(self):
        # GIVEN
        valeur_cible = 100
        repartition_exacte = {'1': {'reprise': 50, 'controle': 0}, '2': {'reprise': 30, 'controle': 0},
                                '3': {'reprise': 20, 'controle': 0}}
        repartition_avec_exces = {'1': {'reprise': 51, 'controle': 0}, '2': {'reprise': 31, 'controle': 0},
                                '3': {'reprise': 20, 'controle': 0}}
        repartition_avec_manque = {'1': {'reprise': 33, 'controle': 0}, '2': {'reprise': 33, 'controle': 0},
                                  '3': {'reprise': 33, 'controle': 0}}
        # Cas théoriquement impossibles car erreur maximum de 1/-1 par agent
        repartition_grand_exces = {'1': {'reprise': 52, 'controle': 0}, '2': {'reprise': 31, 'controle': 0},
                                '3': {'reprise': 21, 'controle': 0}}
        repartition_grand_manque = {'1': {'reprise': 31, 'controle': 0}, '2': {'reprise': 31, 'controle': 0},
                                   '3': {'reprise': 31, 'controle': 0}}
        type_fiche = 'reprise'
        # WHEN
        proposition_exacte = self.service._AffectationService__corriger_arrondis(valeur_cible, repartition_exacte,
                                                                                 type_fiche)
        proposition_exces = self.service._AffectationService__corriger_arrondis(valeur_cible, repartition_avec_exces,
                                                                                 type_fiche)
        proposition_manque = self.service._AffectationService__corriger_arrondis(valeur_cible, repartition_avec_manque,
                                                                                 type_fiche)
        proposition_grand_exces = self.service._AffectationService__corriger_arrondis(valeur_cible,
                                                                                     repartition_grand_exces,
                                                                                 type_fiche)
        proposition_grand_manque = self.service._AffectationService__corriger_arrondis(valeur_cible,
                                                                                      repartition_grand_manque,
                                                                                      type_fiche)
        # THEN
        self.assertEqual({'1': {'reprise': 50, 'controle': 0}, '2': {'reprise': 30, 'controle': 0},
                          '3': {'reprise': 20, 'controle': 0}}, proposition_exacte)
        self.assertEqual({'1': {'reprise': 50, 'controle': 0}, '2': {'reprise': 30, 'controle': 0},
                          '3': {'reprise': 20, 'controle': 0}}, proposition_exces)
        self.assertEqual({'1': {'reprise': 33, 'controle': 0}, '2': {'reprise': 33, 'controle': 0},
                          '3': {'reprise': 34, 'controle': 0}}, proposition_manque)
        self.assertEqual({'1': {'reprise': 50, 'controle': 0}, '2': {'reprise': 30, 'controle': 0},
                          '3': {'reprise': 20, 'controle': 0}}, proposition_grand_exces)
        self.assertEqual({'1': {'reprise': 33, 'controle': 0}, '2': {'reprise': 33, 'controle': 0},
                          '3': {'reprise': 34, 'controle': 0}}, proposition_grand_manque)

    @mock.patch.dict(os.environ, {"PSYCOQUAC_ENGINE": "PostgreSQL"})
    @mock.patch('DataLayer.DAO.dao_fiche_adresse.DAOFicheAdresse.obtenir_statistiques')
    @mock.patch('DataLayer.DAO.dao_agent.DAOAgent.recuperer_quotite')
    def test_obtenir_charge_actuelle(self, mock_recuperer_quotite, mock_obtenir_statistiques):
        # GIVEN
        mock_recuperer_quotite.side_effect = [0.5, 1, 1]
        mock_obtenir_statistiques.side_effect = [[[13]], [[7]], [[50]], [[30]], [[80]], [[40]]]
        agents = [1, 2, 3]
        # WHEN
        charge_actuelle = self.service.obtenir_charge_actuelle(agents)
        # THEN
        self.assertEqual({'1': {'actuelle': 0.2, 'quotite': 0.5}, '2': {'actuelle': 0.8, 'quotite': 1.0},
                          '3': {'actuelle': 1.2, 'quotite': 1.0}}, charge_actuelle)

    @mock.patch.dict(os.environ, {"PSYCOQUAC_ENGINE": "PostgreSQL"})
    @mock.patch('DataLayer.DAO.dao_fiche_adresse.DAOFicheAdresse.obtenir_statistiques')
    @mock.patch('DataLayer.DAO.dao_agent.DAOAgent.recuperer_quotite')
    def test_proposer_repartition(self, mock_recuperer_quotite, mock_obtenir_statistiques):
        # GIVEN
        mock_recuperer_quotite.side_effect = [1, 1]
        mock_obtenir_statistiques.side_effect = [[[25]], [[0]], [[50]], [[0]], [[50]], [[75]]]
        lot = 5
        agents = [1, 2]
        # WHEN
        proposition_repartition = self.service.proposer_repartition(lot, agents)
        # THEN
        mock_recuperer_quotite.assert_any_call(2)
        mock_obtenir_statistiques.assert_any_call(filtre_pot=1, filtre_code_resultat="TR")
        mock_obtenir_statistiques.assert_any_call(filtre_lot=5, filtre_code_resultat="TH")
        self.assertEqual({'1': {'reprise': 50, 'controle': 25}, '2': {'reprise': 25, 'controle': 25}},
                         proposition_repartition)

    def test_echantilloner_fiches(self):
        # GIVEN
        fiche_adresse1 = FicheAdresse(1, 1, 1, Adresse(29, "rue de Raymond Poincaré", 93330, "NEUILLY-SUR-MARNE"),
                                      code_res='TH')
        fiche_adresse2 = FicheAdresse(2, 1, 1, Adresse(21, "Rue de Strasbourg", 93390, "CLICHY-SOUS-BOIS"),
                                      code_res='TH')
        fiche_adresse3 = FicheAdresse(3, 1, 1, Adresse(50, "rue des Lacs", 78800, "HOUILLES"),
                                      code_res='TH')
        fiche_adresse4 = FicheAdresse(4, 1, 1, Adresse(23, "avenue du Marechal Juin", 50000, "SAINT-LÔ"),
                                      code_res='TH')
        fiche_adresse5 = FicheAdresse(5, 1, 1, Adresse(46, "rue du Clair Bocage", 85000, "LA ROCHE-SUR-YON"),
                                      code_res='TH')
        fiche_adresse6 = FicheAdresse(6, 1, 1, Adresse(80, "rue Petite Fusterie", "01000", "BOURG-EN-BRESSE"),
                                      code_res='TH')
        fiche_adresse7 = FicheAdresse(7, 1, 1, Adresse(80, "rue de Raymond Poincaré", 11100, "NARBONNE"),
                                      code_res='TH')
        fiche_adresse8 = FicheAdresse(8, 1, 1, Adresse(95, "rue des lieutemants Thomazo", "04000", "DIGNE-LES-BAINS"),
                                      code_res='TH')
        fiche_adresse9 = FicheAdresse(9, 1, 1, Adresse(15, "avenue de Provence", 26000, "VALENCE"),
                                      code_res='TH')
        fiche_adresse10 = FicheAdresse(10, 1, 1, Adresse(44, "boulevard Aristide Briand", 71200, "LE CREUSOT"),
                                      code_res='TH')
        lot = [fiche_adresse1, fiche_adresse2, fiche_adresse3, fiche_adresse4, fiche_adresse5, fiche_adresse6,
               fiche_adresse7, fiche_adresse8, fiche_adresse9, fiche_adresse10]
        seed(1)
        # WHEN
        lot_controle, lot_validation = self.service.echantilloner_fiches(lot, 5)
        # THEN
        self.assertTrue(fiche_adresse3 in lot_controle)
        self.assertTrue(fiche_adresse8 in lot_validation)
        self.assertTrue(fiche_adresse5.code_res == 'TC')
        self.assertTrue(fiche_adresse10.code_res == 'VA')
        self.assertEqual(5, len(lot_controle))

    @mock.patch.dict(os.environ, {"PSYCOQUAC_ENGINE": "PostgreSQL"})
    @mock.patch('DataLayer.DAO.dao_fiche_adresse.DAOFicheAdresse.recuperer_lot')
    @mock.patch('DataLayer.DAO.dao_fiche_adresse.DAOFicheAdresse.modifier_fiche_adresse')
    def test_appliquer_repartition(self, mock_modifier_fiche_adresse, mock_recuperer_lot):
        # GIVEN
        fiche_adresse1 = FicheAdresse(1, 1, 1, Adresse(29, "rue de Raymond Poincaré", 93330, "NEUILLY-SUR-MARNE"),
                                      code_res='TR')
        fiche_adresse2 = FicheAdresse(2, 1, 1, Adresse(21, "Rue de Strasbourg", 93390, "CLICHY-SOUS-BOIS"),
                                      code_res='TR')
        fiche_adresse3 = FicheAdresse(3, 1, 1, Adresse(50, "rue des Lacs", 78800, "HOUILLES"),
                                      code_res='TR')
        fiche_adresse4 = FicheAdresse(4, 1, 1, Adresse(23, "avenue du Marechal Juin", 50000, "SAINT-LÔ"),
                                      code_res='TR')
        fiche_adresse5 = FicheAdresse(5, 1, 1, Adresse(46, "rue du Clair Bocage", 85000, "LA ROCHE-SUR-YON"),
                                      code_res='TR')
        fiche_adresse6 = FicheAdresse(6, 1, 1, Adresse(80, "rue Petite Fusterie", "01000", "BOURG-EN-BRESSE"),
                                      code_res='TH')
        fiche_adresse7 = FicheAdresse(7, 1, 1, Adresse(80, "rue de Raymond Poincaré", 11100, "NARBONNE"),
                                      code_res='TH')
        fiche_adresse8 = FicheAdresse(8, 1, 1, Adresse(95, "rue des lieutemants Thomazo", "04000", "DIGNE-LES-BAINS"),
                                      code_res='TH')
        fiche_adresse9 = FicheAdresse(9, 1, 1, Adresse(15, "avenue de Provence", 26000, "VALENCE"),
                                      code_res='TH')
        fiche_adresse10 = FicheAdresse(10, 1, 1, Adresse(44, "boulevard Aristide Briand", 71200, "LE CREUSOT"),
                                       code_res='TH')
        lot = [fiche_adresse1, fiche_adresse2, fiche_adresse3, fiche_adresse4, fiche_adresse5, fiche_adresse6,
               fiche_adresse7, fiche_adresse8, fiche_adresse9, fiche_adresse10]
        lot_sauvegarde = []
        id_lot = 1
        repartition = {'1': {'reprise': 3, 'controle': 2}, '2': {'reprise': 2, 'controle': 1}}
        mock_recuperer_lot.return_value = lot
        mock_modifier_fiche_adresse.side_effect = lambda call_args: lot_sauvegarde.append(call_args) or True
        seed(1)
        # WHEN
        resultat = self.service.appliquer_repartition(id_lot, repartition, False)
        #THEN
        self.assertTrue(resultat)
        self.assertEqual(5, sum([1 if fiche.code_res == 'TR' else 0 for fiche in lot_sauvegarde]))
        self.assertEqual(3, sum([1 if fiche.code_res == 'TC' else 0 for fiche in lot_sauvegarde]))
        self.assertEqual(1, lot_sauvegarde[0].agent_id)
        self.assertEqual(2, lot_sauvegarde[5].agent_id)
        self.assertEqual('TR', lot_sauvegarde[1].code_res)
        self.assertEqual('TC', lot_sauvegarde[7].code_res)
        self.assertEqual('VA', lot_sauvegarde[9].code_res)

    @mock.patch.dict(os.environ, {"PSYCOQUAC_ENGINE": "PostgreSQL"})
    @mock.patch('DataLayer.DAO.dao_fiche_adresse.DAOFicheAdresse.obtenir_statistiques')
    def test_lot_a_affecter(self, mock_obtenir_statistiques):
        # GIVEN
        mock_obtenir_statistiques.side_effect = ([[1], [2], [3], [4], [5]], [[2], [4], [5]])
        id_superviseur = 10
        # WHEN
        lots = self.service.lots_a_affecter(id_superviseur)
        #THEN
        self.assertEqual([1, 3], lots)
        self.assertEqual(2, mock_obtenir_statistiques.call_count)
        mock_obtenir_statistiques.assert_called_with(par_lot=True, filtre_pot=-id_superviseur,
                                                     filtre_code_resultat='TA')
