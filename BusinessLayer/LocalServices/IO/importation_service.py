from utils.singleton import Singleton
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
import BusinessLayer.LocalServices.IO.factory_handler as factory
import pathlib


class ImportationService(metaclass=Singleton):

    def importer_lot(self, id_agent, chemin_fichier):
        path = pathlib.Path(chemin_fichier)
        handler = factory.HandlerFactory.get_handler_from_ext(path.suffixes[-1])
        id_lot = DAOFicheAdresse().recuperer_dernier_id_lot() + 1
        liste_fa = handler.import_from_file(chemin_fichier, id_agent, id_lot)
