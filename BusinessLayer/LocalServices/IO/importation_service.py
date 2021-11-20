from BusinessLayer.BusinessObjects.modele import Modele
from utils.singleton import Singleton
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
import BusinessLayer.LocalServices.IO.factory_handler as factory

from typing import Tuple
import pathlib


class ImportationService(metaclass=Singleton):
    @staticmethod
    def importer_lot(id_superviseur: int, chemin_fichier: str, modele: Modele) -> Tuple[int, bool]:
        path = pathlib.Path(chemin_fichier)
        handler = factory.HandlerFactory.get_handler_from_ext(path.suffix)
        id_lot = DAOFicheAdresse().recuperer_dernier_id_lot() + 1
        liste_fa = handler.import_from_file(chemin_fichier, id_superviseur, id_lot, modele)
        res = True
        for fa in liste_fa:
            if fa.adresse_initiale.voie is not None and (
                    fa.adresse_initiale.cp is not None or fa.adresse_finale.ville is not None):
                fa.code_res = "TA"
            else:
                fa.code_res = "DI"
            new_res = DAOFicheAdresse().creer_fiche_adresse(fa)
            res = res * new_res
        DAOFicheAdresse().incrementer_id_lot()
        return id_lot, res
