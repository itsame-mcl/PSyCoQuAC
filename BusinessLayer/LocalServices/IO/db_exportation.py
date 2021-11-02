from BusinessLayer.LocalServices.IO.csv_exportation import CSVExportation

class DBExportation:

    def __init__(self, type_fichier):
        if type_fichier == "CSV":
            self.__type_fichier = CSVExportation()
        self.__exportation = self.__type_fichier.exportation

    @property
    def exportation(self):
        """
        return the opened connection.

        :return: the opened connection.
        """
        return self.__exportation
        