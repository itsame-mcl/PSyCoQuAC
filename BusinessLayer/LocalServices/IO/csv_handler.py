from BusinessLayer.LocalServices.IO.abstract_handler import AbstractHandler
from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from BusinessLayer.BusinessObjects.adresse import Adresse
from BusinessLayer.BusinessObjects.modele import Modele
from typing import List
import csv


class CSVHandler(AbstractHandler):
    def import_from_file(self, path, id_superviseur: int, id_lot: int, model: Modele,
                         encoding: str = 'utf-8') -> List[FicheAdresse]:
        """
        Cette méthode permet d'importer un fichier dans l'application PSyCoQuAC,
        en se basant sur un modèle pré-existant afin de faciliter l'importation.

        :param path:
        le chemin, sur la machine de l'utilisateur, du fichier à importer 
        :param id_superviseur:
        l'identifiant, dans la base de données Agents, du superviseur qui importe le fichier
        :param id_lot:
        l'identifiant de lot, dans la base de données FA, des fiches adresse importées dans le fichier
        :param model:
        le modèle de fichier correspondant au fichier à importer
        :param encoding:
        le codage de caractères du fichier à importer
        :return:
        renvoie la liste de fiches adresse contenues dans le fichier importé
        """
        # Ouverture du fichier pour importation
        with open(path, 'r', encoding=encoding) as file:
            reader = csv.reader(file, delimiter=';')
            liste_fa = []
            next(reader)
            for row in reader:
                numero = [str(row[index]) for index in model.correspondances.position_numero]
                voie = [str(row[index]) for index in model.correspondances.position_voie]
                cp = [str(row[index]) for index in model.correspondances.position_cp]
                ville = [str(row[index]) for index in model.correspondances.position_ville]
                donnees_supplementaires = dict()
                for cle, position in model.correspondances.positions_supplementaires.items():
                    donnees_supplementaires[cle] = str(row[position])
                adresse = Adresse(' '.join(numero), ' '.join(voie), ' '.join(cp), ' '.join(ville))
                fa = FicheAdresse(0, id_superviseur, id_lot, adresse, champs_supplementaires=donnees_supplementaires)
                liste_fa.append(fa)
        return liste_fa

    def export_to_file(self, lot: List[FicheAdresse], path: str):
        """
        Cette méthode permet d'exporter un lot de fiches adresse.

        :param lot:
        le lot (c'est-à-dire une liste de fiches adresse) à exporter
        :param path:
        le chemin, sur la machine de l'utilisateur, où ce dernier souhaite placer le lot exporté
        """
        with open(path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, lot[0].as_dict(True).keys())
            writer.writeheader()
            for fiche in lot:
                writer.writerow(fiche.as_dict(True))
