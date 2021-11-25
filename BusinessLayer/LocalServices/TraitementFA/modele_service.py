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
        """
        Cette méthode permet d'identifier le modèle d'importation correspondant au fichier
        dont on renseigne le chemin sur la machine de l'utilisateur.


        :param chemin_fichier:
        le chemin, sur la machine de l'utilisateur, du fichier dont cherche à identifier le modèle d'importation
        :return:
        renvoie le modèle de fichier auquel correspond le fichier
        """
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
        """
        Cette méthode permet de créer un modèle de fichier à importer,
        en renseignant la position des colonnes contenant les informations des adresses contenues dans le fichier.

        :param nom:
        le nom du modèle que l'on crée
        :param regex:
        l'expression régulière présente dans le nom du fichier ayant créé le modèle, afin de détecter les autres fichiers suivant ce modèle
        :param positions_numero:
        le numéro, dans le fichier, de la (ou des) colonne(s) contenant le numéro des adresses du fichier
        :param positions_voie:
        le numéro, dans le fichier, de la (ou des) colonne(s) contenant le type de voie (rue, impasse, avenue, boulevard) des adresses du fichier
        :param positions_cp:
        le numéro, dans le fichier, de la (ou des) colonne(s) contenant le code postal des adresses du fichier
        :param positions_ville:
        le numéro, dans le fichier, de la (ou des) colonne(s) contenant la ville des adresses du fichier
        :param positions_sup:
        le numéro, dans le fichier, de la (ou des) colonne(s) contenant des informations supplémentaires des adresses.
        :return:
        renvoie un booléen valant True si le modèle a été correctement créé
        """
        correspondances = Correspondance(tuple(positions_numero), tuple(positions_voie),
                                         tuple(positions_cp), tuple(positions_ville), positions_sup)
        modele = Modele(nom, regex, correspondances)
        res = DAOModele().creer_modele(modele)
        return res
