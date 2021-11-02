from BusinessLayer.LocalServices.IO.interface_importation import InterfaceImportation
from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
import csv
from DataLayer import DAO as dao

class CSVImportation(InterfaceImportation): # Il manque le rôle des modèles, qui interviennent lors de l'importation

    def importer_lot(session_utilisateur, id_lot, chemin_vers_fichier):
        file = open(chemin_vers_fichier, 'r')
        reader = csv.DictReader(file, delimiter=';')
        liste_fiche_adresse = []
        agent_id = session_utilisateur.utilisateur_connecte.agent_id
        lot_id = dao.recuperer_id_lot
        for row in reader:
            liste_fiche_adresse.append({'numero': str(row['%num%']), 'nom_voie': str(row['%voie%']), 'code_postal': str(row['%']), 'nom_commune': str(row['nom'])})
        file.close()
        for elt in liste_fiche_adresse:
            fiche_id = dao.recuperer_id_fiche_adresse
            adresse_initiale = elt['numero'] + elt['nom_voie'] + elt['code_postal'] + elt['nom_commune']
            dao.DAOFicheAdresse.creer_fiche_adresse(FicheAdresse(fiche_id, agent_id, lot_id, adresse_initiale))