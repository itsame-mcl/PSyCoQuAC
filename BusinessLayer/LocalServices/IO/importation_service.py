from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from BusinessLayer.BusinessObjects.modele import Modele
from utils.singleton import Singleton
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
from BusinessLayer.WebServices.BANClient import BANClient
import BusinessLayer.LocalServices.IO.factory_handler as factory
from typing import Tuple
import pathlib
import chardet


class ImportationService(metaclass=Singleton):
    @staticmethod
    def _filtre_fiche_importation(fiche: FicheAdresse) -> bool:
        """

        :param fiche:
        la fiche adresse à filtrer lors de l'importation
        :return:
        renvoie un booléen valant True si la fiche adresse est géolocalisable par l'API
        """
        num = fiche.adresse_initiale.numero
        voie = fiche.adresse_initiale.voie
        cp = fiche.adresse_initiale.cp
        ville = fiche.adresse_initiale.ville
        if (num is None or num in ["", " "]) and (voie is None or voie in ["", " "]):
            return False
        if (cp is None or cp in ["", " "]) and (ville is None or ville in ["", " "]):
            return False
        return True

    def importer_lot(self, id_superviseur: int, chemin_fichier: str, modele: Modele,
                     filtrer: bool = True) -> Tuple[int, bool]:
        """
        Cette méthode permet d'importer un fichier dans l'application PSyCoQuAC,
        en se basant sur un modèle pré-existant afin de faciliter l'importation.

        :param id_superviseur:
        l'identifiant, dans la base de données Agents, du superviseur qui importe le fichier
        :param chemin_fichier:
        le chemin, sur la machine de l'utilisateur, du fichier à importer
        :param modele:
        le modèle de fichier correspondant au fichier à importer
        :param filtrer:
        un booléen valant True si la fiche adresse dans le lot importé peut être traitée par l'API
        :return:
        renvoie la liste de fiches adresse contenues dans le fichier importé
        """
        path = pathlib.Path(chemin_fichier)
        try:
            handler = factory.HandlerFactory.get_handler_from_ext(path.suffix)
            # Première ouverture du fichier pour détecter le type d'encodage
            raw = open(path, "rb").read()
            res = chardet.detect(raw)
            id_lot = DAOFicheAdresse().recuperer_dernier_id_lot() + 1
            liste_fa = handler.import_from_file(chemin_fichier, id_superviseur * -1, id_lot, modele, res['encoding'])
            for fa in liste_fa:
                if not filtrer or self._filtre_fiche_importation(fa):
                    fa.code_res = "TA"
                else:
                    fa.agent_id = id_superviseur
                    fa.code_res = "EF"
            res = DAOFicheAdresse().creer_multiple_fiche_adresse(liste_fa)
            DAOFicheAdresse().incrementer_id_lot()
        except AttributeError:
            print("Fichiers " + str(path.suffix)[1:] + " non supportés.")
            id_lot = None
            res = False
        return id_lot, res

    @staticmethod
    def lots_a_traiter_api(id_superviseur: int):
        """
        Cette méthode permet de récupérer les lots (c'est-à-dire les listes de fiches adresse) à traiter par l'API,
        parmi les lots du superviseur dont on renseigne l'identifiant de la base de données Agents.

        :param id_superviseur:
        l'identifiant, dans la base de données Agents, du superviseur dont on souhaite connaître
        la liste de lots à traiter par l'API
        :return:
        renvoie la liste des lots du superviseur étant à traiter par l'API
        """
        lots = []
        res = DAOFicheAdresse().obtenir_statistiques(par_lot=True, filtre_pot=-id_superviseur,
                                                     filtre_code_resultat="TA")
        for ligne in res:
            lots.append(ligne[0])
        return lots

    @staticmethod
    def traiter_lot_api(id_lot: int, verbose=False):
        """
        Cette méthode permet de traiter un lot (c'est-à-dire une liste de fiches adresse),
        dont on renseigne l'identifiant de la base de données FA, par l'API.

        :param id_lot:
        l'identifiant de lot, dans la base de données FA, des fiches adresse à traiter par l'API 
        :param verbose:
        un booléen valant True si le traitement de la fiche adresse par l'API prend du temps
        :return:
        renvoie un booléen valant True si le lot a été correctement traité par l'API
        """
        if verbose:
            print("Chargement du lot à traiter...")
        lot = DAOFicheAdresse().recuperer_lot(id_lot)
        fiches_a_traiter = []
        for fiche in lot:
            if fiche.code_res == "TA":
                fiches_a_traiter.append(fiche)
        fiches_traitees = BANClient().geocodage_par_lot(fiches_a_traiter, verbose=verbose)
        res = True
        if verbose:
            print("Enregistrement des résultats du traitement...")
            res = DAOFicheAdresse().modifier_multiple_fiche_adresse(fiches_traitees)
        if verbose:
            print("Traitement du lot terminé !")
        return res
