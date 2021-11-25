import BusinessLayer.LocalServices.IO.factory_handler as factory
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
from utils.singleton import Singleton

import pathlib


class ExportationService(metaclass=Singleton):

    @staticmethod
    def exporter_lot(id_lot, chemin_fichier):
        """
        Cette méthode permet d'exporter un lot de fiches adresse.

        :param id_lot:
        l'identifiant de lot, dans la base de données FA, des fiches adresse à exporter
        :param chemin_fichier:
        le chemin, sur la machine de l'utilisateur, où ce dernier souhaite placer le lot exporté
        """
        path = pathlib.Path(chemin_fichier).resolve()
        try:
            handler = factory.HandlerFactory.get_handler_from_ext(path.suffix)
            path.touch(exist_ok=True)
            lot = DAOFicheAdresse().recuperer_lot(id_lot)
            handler.export_to_file(lot, chemin_fichier)
        except AttributeError:
            print("Fichiers " + str(path.suffix)[1:] + " non supportés.")
