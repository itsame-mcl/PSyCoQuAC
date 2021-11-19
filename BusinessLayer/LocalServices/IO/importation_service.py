from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from BusinessLayer.BusinessObjects.modele import Modele
from utils.singleton import Singleton
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
from DataLayer.DAO.dao_modele import DAOModele
import BusinessLayer.LocalServices.IO.factory_handler as factory
from BusinessLayer.WebServices.BANClient import BANClient

from typing import List
import pathlib
import re


class ImportationService(metaclass=Singleton):
    def __identifier_modele(self, nom_fichier) -> Modele:
        id_modele = 1
        liste_modeles = DAOModele().recuperer_regex()
        for modele, regex in liste_modeles:
            match = re.match(re.compile(regex), nom_fichier)
            if match:
                id_modele = modele
        model_object = DAOModele().recuperer_modele(id_modele)
        return model_object

    def __charger_lot(self, id_superviseur, chemin_fichier) -> List[FicheAdresse]:
        path = pathlib.Path(chemin_fichier)
        handler = factory.HandlerFactory.get_handler_from_ext(path.suffixes[-1])
        id_lot = DAOFicheAdresse().recuperer_dernier_id_lot() + 1
        modele = self.__identifier_modele(path.name)
        liste_fa = handler.import_from_file(chemin_fichier, id_superviseur, id_lot, modele)
        return liste_fa

    def importer_lot(self, id_superviseur, chemin_fichier, seuil_score : float = 0.9):
        liste_fa = self.__charger_lot(id_superviseur, chemin_fichier)
        for fa in liste_fa:
            if fa.adresse_initiale.voie is not None and (fa.adresse_initiale.cp is not None or fa.adresse_finale.ville is not None):
                fa.code_res = "TA"
                score, fa = BANClient().geocodage_par_fiche(fa)
                if score > seuil_score:
                    fa.code_res = "TH"
                else:
                    fa.code_res = "TR"
            else:
                fa.code_res = "DI"
            DAOFicheAdresse().creer_fiche_adresse(fa)
        DAOFicheAdresse().incrementer_id_lot()
