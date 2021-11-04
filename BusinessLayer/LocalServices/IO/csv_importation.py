from BusinessLayer.LocalServices.IO.interface_importation import InterfaceImportation
from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from BusinessLayer.BusinessObjects.modele import Modele
from BusinessLayer.BusinessObjects.correspondance import Correspondance
from BusinessLayer.BusinessObjects.agent import Agent
import csv
from DataLayer import DAO as dao

class CSVImportation(InterfaceImportation): # Il manque le rôle des modèles, qui interviennent lors de l'importation

    def importer_lot(self, agent : Agent, id_lot : int, chemin_fichier):
        pass
        # Si le modèle est connu, on importe le lot comme les autres lots de son modèle
        # Si le modèle est inconnu, on fait appel à la méthode importer_lot_inconnu
    
    def importer_lot_inconnu(self, agent : Agent, id_lot : int, chemin_fichier):
        file = open(chemin_fichier, 'r')
        reader = csv.DictReader(file, delimiter=';')
        liste_fiche_adresse = []
        id_agent = agent.agent_id
        for row in reader:
            liste_fiche_adresse.append({'numero': str(row['%num%']), 'nom_voie': str(row['%voie%']), 'code_postal': str(row['%post%']), 'nom_commune': str(row['%nom%'])})
        file.close()
        correspondance = Correspondance(row['%num%'], row['%voie%'], row['%post%'], row['%nom%'])
        dao.DAOModele.creer_modele(Modele())
        for elt in liste_fiche_adresse:
            fiche_id = dao.recuperer_id_fiche_adresse
            adresse_initiale = elt['numero'] + elt['nom_voie'] + elt['code_postal'] + elt['nom_commune']
            dao.DAOFicheAdresse.creer_fiche_adresse(FicheAdresse(fiche_id, id_agent, id_lot, adresse_initiale))