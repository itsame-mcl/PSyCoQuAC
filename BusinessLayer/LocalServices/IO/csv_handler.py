from BusinessLayer.LocalServices.IO.abstract_handler import AbstractHandler
from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from BusinessLayer.BusinessObjects.adresse import Adresse
from BusinessLayer.BusinessObjects.modele import Modele
from BusinessLayer.BusinessObjects.correspondance import Correspondance
from BusinessLayer.BusinessObjects.agent import Agent
from typing import List
import csv


class CSVHandler(AbstractHandler):
    def import_from_file(self, path, id_agent: int, id_lot: int, model: Modele) -> List[FicheAdresse]:
        file = open(path, 'r')
        reader = csv.reader(file, delimiter=';')
        liste_fa = []
        for row in reader:
            adresse = Adresse(row[model.correspondances.position_numero], row[model.correspondances.position_voie],
                              row[model.correspondances.position_cp], row[model.correspondances.position_ville])
            fa = FicheAdresse(0, id_agent, id_lot, adresse)
            liste_fa.append(fa)
        return liste_fa

