from typing import List, Dict

from BusinessLayer.BusinessObjects.correspondance import Correspondance
from BusinessLayer.BusinessObjects.modele import Modele
from utils.singleton import Singleton
from DataLayer.DAO.dao_modele import DAOModele

import pathlib
import re


class ModeleService(metaclass=Singleton):
    @staticmethod
    def identifier_modele(chemin_fichier) -> Modele:
        path = pathlib.Path(chemin_fichier)
        nom_fichier = path.name
        id_modele = 0
        liste_modeles = DAOModele().recuperer_regex()
        for modele, regex in liste_modeles.items():
            match = re.match(re.compile(regex), nom_fichier)
            if match:
                id_modele = modele
        if id_modele > 0:
            model_object = DAOModele().recuperer_modele(id_modele)
        else:
            model_object = None
        return model_object

    @staticmethod
    def creer_modele(nom: str, regex: str, positions_numero: List[int], positions_voie: List[int],
                     positions_cp: List[int], positions_ville: List[int], positions_sup: Dict) -> bool:
        correspondances = Correspondance(tuple(positions_numero), tuple(positions_voie),
                                         tuple(positions_cp), tuple(positions_ville), positions_sup)
        modele = Modele(nom, regex, correspondances)
        res = DAOModele().creer_modele(modele)
        return res
