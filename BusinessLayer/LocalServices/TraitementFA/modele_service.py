from BusinessLayer.BusinessObjects.modele import Modele
from utils.singleton import Singleton
from DataLayer.DAO.dao_modele import DAOModele

import pathlib
import re


class ModeleService(metaclass=Singleton):
    def identifier_modele(self, chemin_fichier) -> Modele:
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
