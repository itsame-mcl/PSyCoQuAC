from BusinessLayer.LocalServices.IO.csv_importation import CSVImportation
from utils.singleton import Singleton
import pathlib

@Singleton
class ImportationServices:

    def __init__(self, chemin_fichier): # Pour l'instant, on part du principe que l'utilisateur connaît le chemin du fichier qu'il souhaite importer
        path = pathlib.Path(chemin_fichier)
        if path.suffixes[-1] == ".csv": # path.suffixes permet de gérer les cas où le chemin a plusieurs suffixes comme extension
            self.__type_fichier = CSVImportation()
        self.__importation = self.__type_fichier.importer_lot()

    @property
    def importation(self):
        """
        return the opened connection.

        :return: the opened connection.
        """
        return self.__importation