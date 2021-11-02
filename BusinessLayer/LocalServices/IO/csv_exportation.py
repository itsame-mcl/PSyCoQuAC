from BusinessLayer.LocalServices.IO.interface_exportation import InterfaceExportation
import pandas as pd
from DataLayer import DAO as dao

class CSVExportation(InterfaceExportation):

    def exporter_lot(session_utilisateur, id_lot, chemin_vers_fichier):
        agent_id = dao.recuperer_agent_id(session_utilisateur.utilisateur_connecte.nom_utilisateur) # On fait appel à une méthode de la DAO qui récupère l'id de l'agent
        lot = dao.recuperer_lot(agent_id, id_lot) # On fait appel à une méthode de la DAO qui récupère tt les fiches adresse d'un lot qui ont été traitées par l'agent X
        df = pd.DataFrame(lot)
        nom_exportation = str(chemin_vers_fichier)+"fichier "+str(id_lot)+".csv"
        df.to_csv(nom_exportation)