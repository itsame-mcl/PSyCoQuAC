from unittest import TestCase
from datetime import date
from BusinessLayer.BusinessObjects.adresse import Adresse
from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse


class TestFicheAdresse(TestCase):
    def test_creer_fiche_importation(self):
        # GIVEN - données générées via https://fr.fakenamegenerator.com/gen-random-fr-fr.php
        adresse_numero = 90
        adresse_voie = "Rue du Limas"
        adresse_code_postal = 20200
        adresse_ville = "BASTIA"
        id_superviseur = 1
        id_lot = 1
        # WHEN
        fiche_adresse = FicheAdresse(0, id_superviseur, id_lot, Adresse(adresse_numero, adresse_voie,
                                                                        adresse_code_postal, adresse_ville))
        code_resultat = fiche_adresse.code_res
        adresse_finale = fiche_adresse.adresse_finale
        coords_wgs84 = fiche_adresse.coords_wgs84
        champs_supplementaires = fiche_adresse.champs_supplementaires
        # THEN
        self.assertEqual("TF", code_resultat)
        self.assertEqual(Adresse(adresse_numero, adresse_voie, adresse_code_postal, adresse_ville), adresse_finale)
        self.assertEqual({}, coords_wgs84)
        self.assertEqual({}, champs_supplementaires)

    def test_creer_fiche_depuis_dictionnaire(self):
        # GIVEN
        donnees = {"identifiant_fa": 872, "identifiant_pot": 3, "identifiant_lot": 1, "code_resultat": "TA",
                   "date_importation": date(2021, 11, 1), "date_dernier_traitement": date(2021, 11, 5),
                   "initial_numero": "59", "initial_voie": "Rue de Verdun", "initial_code_postal": "91230",
                   "initial_ville": "MONTGERON", "final_numero": "59", "final_voie": "Rue de Verdun",
                   "final_code_postal": "91230", "final_ville": "MONTGERON", "coordonnees_wgs84": {},
                   "champs_supplementaires": {'identifiant': 'FA872'}}
        # WHEN
        fiche_adresse = FicheAdresse.from_dict(donnees)
        code_resultat = fiche_adresse.code_res
        adresse_finale = fiche_adresse.adresse_finale
        champs_supplementaires = fiche_adresse.champs_supplementaires
        # THEN
        self.assertEqual("TA", code_resultat)
        self.assertEqual(Adresse(59, "Rue de Verdun", 91230, "MONTGERON"), adresse_finale)
        self.assertEqual("FA872", champs_supplementaires['identifiant'])

    def test_transitions_code_resultat(self):
        # GIVEN
        donnees = {"identifiant_fa": 872, "identifiant_pot": 3, "identifiant_lot": 1, "code_resultat": "TH",
                   "date_importation": date(2021, 11, 1), "date_dernier_traitement": date(2021, 11, 5),
                   "initial_numero": "59", "initial_voie": "Rue de Verdun", "initial_code_postal": "91230",
                   "initial_ville": "MONTGERON", "final_numero": "59", "final_voie": "Rue de Verdun",
                   "final_code_postal": "91230", "final_ville": "MONTGERON", "coordonnees_wgs84": {},
                   "champs_supplementaires": {'identifiant': 'FA872'}}
        # WHEN
        fiche_adresse = FicheAdresse.from_dict(donnees)
        fiche_adresse.code_res = "TC"
        # THEN
        self.assertEqual("TC", fiche_adresse.code_res)
        self.assertRaises(ValueError, setattr, fiche_adresse, 'code_res', 'DF')
