from BusinessLayer.BusinessObjects.modele import Modele
from utils.singleton import Singleton
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
from BusinessLayer.WebServices.BANClient import BANClient
import BusinessLayer.LocalServices.IO.factory_handler as factory
from utils.progress_bar import printProgressBar
from typing import Tuple
import pathlib


class ImportationService(metaclass=Singleton):
    @staticmethod
    def importer_lot(id_superviseur: int, chemin_fichier: str, modele: Modele) -> Tuple[int, bool]:
        path = pathlib.Path(chemin_fichier)
        handler = factory.HandlerFactory.get_handler_from_ext(path.suffix)
        id_lot = DAOFicheAdresse().recuperer_dernier_id_lot() + 1
        liste_fa = handler.import_from_file(chemin_fichier, id_superviseur * -1, id_lot, modele)
        res = True
        for fa in liste_fa:
            if fa.adresse_initiale.voie is not None and (
                    fa.adresse_initiale.cp is not None or fa.adresse_finale.ville is not None):
                fa.code_res = "TA"
            else:
                fa.code_res = "DI"
        res = DAOFicheAdresse().creer_multiple_fiche_adresse(liste_fa)
        DAOFicheAdresse().incrementer_id_lot()
        return id_lot, res

    @staticmethod
    def traiter_lot_api(id_lot: int, verbose=False):
        if verbose:
            print("Chargement du lot à traiter...")
        lot = DAOFicheAdresse().recuperer_lot(id_lot)
        fiches_a_traiter = list()
        for fiche in lot:
            if fiche.code_res == "TA":
                fiches_a_traiter.append(fiche)
        fiches_traitees = BANClient().geocodage_par_lot(fiches_a_traiter, verbose=True)
        index = 0
        res = True
        if verbose:
            print("Enregistrement des résultats du traitement...")
        for fiche in fiches_traitees:
            new_res = DAOFicheAdresse().modifier_fiche_adresse(fiche)
            res = res * new_res
            if verbose:
                index += 1
                printProgressBar(index, len(fiches_traitees),
                                 prefix='Progression :', suffix='terminé', length=50)
        if verbose:
            print("Enregistrement terminé !")
        return res
