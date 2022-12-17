from unittest import TestCase
from BusinessLayer.BusinessObjects.adresse import Adresse


class TestAdresse(TestCase):
    def setUp(self) -> None:
        self.PLACE_STANISLAS = "Place Stanislas"

    def test_creer_adresse(self):
        # GIVEN - données générées via https://fr.fakenamegenerator.com/gen-random-fr-fr.php
        adresse_numero = '90'
        adresse_voie = self.PLACE_STANISLAS
        adresse_code_postal = '44100'
        adresse_ville = "NANTES"
        # WHEN
        adresse = Adresse(adresse_numero, adresse_voie, adresse_code_postal, adresse_ville)
        numero = adresse.numero
        voie = adresse.voie
        cp = adresse.cp
        ville = adresse.ville
        # THEN
        self.assertIsInstance(adresse, Adresse)
        self.assertEqual("90", numero)
        self.assertEqual(self.PLACE_STANISLAS, voie)
        self.assertEqual("44100", cp)
        self.assertEqual("NANTES", ville)

    def test_chaine_adresse(self):
        # GIVEN - données générées via https://fr.fakenamegenerator.com/gen-random-fr-fr.php
        adresse_numero = '49'
        adresse_voie = "Place Napoléon"
        adresse_code_postal = '59130'
        adresse_ville = "LAMBERSART"
        # WHEN
        adresse = Adresse(adresse_numero, adresse_voie, adresse_code_postal, adresse_ville)
        chaine = str(adresse)
        # THEN
        self.assertEqual("49 Place Napoléon 59130 LAMBERSART", chaine)

    def test_egalite_adresses(self):
        # GIVEN
        adresse1_numero = '90'
        adresse1_voie = self.PLACE_STANISLAS
        adresse1_code_postal = '44100'
        adresse1_ville = "NANTES"
        adresse2_numero = '49'
        adresse2_voie = "Place Napoléon"
        adresse2_code_postal = '59130'
        adresse2_ville = "LAMBERSART"
        # WHEN
        adresse1 = Adresse(adresse1_numero, adresse1_voie, adresse1_code_postal, adresse1_ville)
        adresse2 = Adresse(adresse2_numero, adresse2_voie, adresse2_code_postal, adresse2_ville)
        # THEN
        self.assertTrue(Adresse('90', self.PLACE_STANISLAS, '44100', "NANTES") == adresse1)
        self.assertFalse(adresse1 == adresse2)
