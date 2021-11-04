from BusinessLayer.LocalServices.IO.interface_exportation import InterfaceExportation
import pandas as pd
from DataLayer import DAO as dao

class CSVExportation(InterfaceExportation):

    def exporter_lot(self, id_lot : int, destination):
        lot = dao.recuperer_lot(id_lot)
        df = pd.DataFrame(lot)
        nom_exportation = str(destination)+"fichier "+str(id_lot)+".csv"
        df.to_csv(nom_exportation)