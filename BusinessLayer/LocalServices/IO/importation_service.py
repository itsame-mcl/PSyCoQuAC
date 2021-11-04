from BusinessLayer.LocalServices.IO.csv_importation import CSVImportation
from utils.singleton import Singleton
from DataLayer import DAO as dao
import pathlib

@Singleton
class ImportationServices:

    def __init__(self, agent, chemin_fichier): # Pour l'instant, on part du principe que l'utilisateur connaît le chemin du fichier qu'il souhaite importer
        path = pathlib.Path(chemin_fichier)
        if path.suffixes[-1] == ".csv": # path.suffixes permet de gérer les cas où le chemin a plusieurs suffixes comme extension
            self.__type_fichier = CSVImportation()
        id_lot = dao.DAOFicheAdresse.recuperer_prochain_id_lot()
        self.__importation = self.__type_fichier.importer_lot(agent, id_lot, chemin_fichier)

    @property
    def importation(self):
        return self.__importation