import BusinessLayer.LocalServices.IO.factory_handler as factory
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
from utils.singleton import Singleton

import pathlib

class ExportationService(metaclass=Singleton):

    def exporter_lot(self, id_lot, chemin_fichier):
        path = pathlib.Path(chemin_fichier)
        handler = factory.HandlerFactory.get_handler_from_ext(path.suffixes[-1])
        lot = DAOFicheAdresse().recuperer_lot(id_lot)
        handler.export_to_file(lot, chemin_fichier)
