from BusinessLayer.LocalServices.IO.csv_exportation import CSVExportation
from utils.singleton import Singleton

@Singleton
class ExportationServices:

    def __init__(self, id_lot, chemin_destination, type_fichier):
        if type_fichier == "CSV":
            self.__type_fichier = CSVExportation()
        self.__exportation = self.__type_fichier.exporter_lot(session_utilisateur, id_lot, chemin_destination)

    @property
    def exportation(self):
        """
        return the opened connection.

        :return: the opened connection.
        """
        return self.__exportation
        