from BusinessLayer.LocalServices.IO.interface_importation import InterfaceImportation
import csv
from DataLayer import DAO as dao

class CSVImportation(InterfaceImportation): # Il manque le rôle des modèles, qui interviennent lors de l'importation

    def importer_lot(session_utilisateur, id_lot, chemin_vers_fichier):
        file = open(chemin_vers_fichier, 'r')
        # crée une liste d'objets FicheAdresse
        reader = csv.DictReader(file, delimiter=';')
        liste_fiche_adresse = []
        for row in reader:
            
            dao.DAOFicheAdresse.creer_fiche_adresse()
        file.close()