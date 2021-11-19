from BusinessLayer.LocalServices.IO.abstract_handler import AbstractHandler
from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from BusinessLayer.BusinessObjects.adresse import Adresse
from BusinessLayer.BusinessObjects.modele import Modele
from typing import List
import csv


class CSVHandler(AbstractHandler):
    def import_from_file(self, path, id_superviseur: int, id_lot: int, model: Modele) -> List[FicheAdresse]:
        with open(path, 'r') as file:
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
        with open(path, 'w') as file:
            writer = csv.DictWriter(file, lot[0].as_dict().keys())
            writer.writeheader()
            for fiche in lot:
                writer.writerow(fiche.as_dict())
