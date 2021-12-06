from typing import List
from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
import DataLayer.DAO.interface_factory as factory
from utils.singleton import Singleton


class DAOFicheAdresse(metaclass=Singleton):
    def __init__(self):
        self.__interface = factory.InterfaceFactory.get_interface("FicheAdresse")

    def recuperer_fiche_adresse(self, identifiant: int) -> FicheAdresse:
        """
        Cette méthode permet de récupérer une fiche adresse de la base de données FA, dont on a renseigné l'identifiant.

        :param identifiant:
        l'identifiant, dans la base de données FA, de la fiche adresse que l'on souhaite récupérer
        :return:
        renvoie le Business Object FicheAdresse correspondant à l'identifiant passé en argument
        """
        data = self.__interface.recuperer_fiche_adresse(identifiant)
        return FicheAdresse.from_dict(data)

    def recuperer_pot(self, identifiant: int) -> List[FicheAdresse]:
        """
        Cette méthode permet de récupérer le pot (c'est-à-dire la liste de fiches adresse à contrôler/reprendre)
        de l'agent dont on a renseigné l'identifiant de la base de données Agents.

        :param identifiant:
        l'identifiant, dans la base de données Agents, de l'agent dont on cherche à récupérer le pot
        :return:
        renvoie la liste des fiches adresse de l'agent dont on a renseigné l'identifiant
        """
        data = self.__interface.recuperer_liste_fiches_adresse(identifiant, -1)
        pot = list()
        for row in data:
            pot.append(FicheAdresse.from_dict(row))
        return pot

    def recuperer_lot(self, identifiant: int) -> List[FicheAdresse]:
        """
        Cette méthode permet de récupérer le lot (c'est-à-dire la liste de fiches adresse importer en même temps)
        dont on a renseigné l'identifiant de la base de données FA.

        :param identifiant:
        l'identifiant de lot, dans la base de données FA, des fiches adresse que l'on souhaite récupérer
        :return:
        renvoie la liste des fiches adresse dont on a renseigné l'identifiant
        """
        data = self.__interface.recuperer_liste_fiches_adresse(-1, identifiant)
        lot = list()
        for row in data:
            lot.append(FicheAdresse.from_dict(row))
        return lot

    def affecter_fiches_adresse(self, identifiant_agent: int, code_resultat: str, liste_fiches_id: List[int]):
        """
        Cette méthode permet d'affecter à un agent (c'est-à-dire de placer dans le pot de cet agent)
        la liste de fiches adresse dont les identifiants ont été renseignées en argument.

        :param identifiant_agent:
        l'identifiant, dans la base de données Agents, de l'agent à qui l'on souhaite affecter des fiches adresse
        :param code_resultat:
        le nouveau code résultat à affecter aux fiches concernées
        :param liste_fiches_id:
        la liste des identifiants, dans la base de données FA, des fiches adresse que l'on souhaite affecter
        :return:
        renvoie un booléen valant True si les fiches adresse ont été correctement affectées à l'agent
        """
        res = self.__interface.modifier_agent_fiches_adresse(identifiant_agent, code_resultat, liste_fiches_id)
        return res

    def creer_fiche_adresse(self, fa: FicheAdresse) -> bool:
        """
        Cette méthode permet de créer un Business Object FicheAdresse pris en argument dans la base de données FA.

        :param fa:
        la fiche adresse que l'on cherche à créer dans la base de données FA
        :return:
        renvoie un booléen valant True si la fiche adresse a été correctement créée dans la base de données FA
        """
        res = self.__interface.creer_fiche_adresse(fa.as_dict())
        return res

    def creer_multiple_fiche_adresse(self, liste_fa: List[FicheAdresse]) -> bool:
        """
        Cette méthode permet de créer une liste de Business Object FicheAdresse prise en argument dans la base de données FA.

        :param liste_fa:
        la liste de fiches adresse que l'on cherche à créer dans la base de données FA
        :return:
        renvoie un booléen valant True si les fiches adresse ont été correctement créées dans la base de données FA
        """
        liste_dict = [fa.as_dict() for fa in liste_fa]
        res = self.__interface.creer_multiple_fiche_adresse(liste_dict)
        return res

    def modifier_fiche_adresse(self, fa: FicheAdresse) -> bool:
        """
        Cette méthode permet de modifier les informations contenant dans une fiche adresse de la base de données FA.

        :param fa:
        la fiche adresse que l'on cherche à modifier dans la base de données FA
        :return:
        renvoie un booléen valant True si la fiche adresse a été correctement modifiée dans la base de données FA
        """
        res = self.__interface.modifier_fiche_adresse(fa.as_dict())
        return res

    def modifier_multiple_fiche_adresse(self, liste_fa: List[FicheAdresse]) -> bool:
        liste_dict = [fa.as_dict() for fa in liste_fa]
        res = self.__interface.modifier_multiple_fiche_adresse(liste_dict)
        return res

    def supprimer_fiche_adresse(self, identifiant: int) -> bool:
        """
        Cette méthode permet de supprimer une fiche adresse de la base de données FA.

        :param identifiant:
        l'identifiant, dans la base de données FA, de la fiche adresse que l'on cherche supprimer de la base de données FA
        :return:
        renvoie un booléen valant True si la fiche adresse a été correctement supprimée de la base de données FA
        """
        res = self.__interface.supprimer_fiche_adresse(identifiant)
        return res

    def obtenir_statistiques(self, par_pot: bool = False, par_lot: bool = False, par_code_resultat: bool = False,
                             filtre_pot: int = None, filtre_lot: int = None,
                             filtre_code_resultat: str = None) -> List[tuple]:
        """
        Cette méthode permet d'obtenir des statistiques par pots/lots/codes résultat selon les paramètres passés en arguments.
        Elle permet également de préciser, au moyen des filtres, 
        les pots/lots/codes résultat pour lesquels on souhaite obtenir des statistiques.

        :param par_pot:
        un booléen valant True si on souhaite obtenir des statistiques par pots
        (c'est-à-dire par listes de fiches adresse à contrôler/reprendre par un agent)
        :param par_lot:
        un booléen valant True si on souhaite obtenir des statistiques par lots
        (c'est-à-dire par listes de fiches adresse importées simultanément)
        :param par_code_resultat:
        un booléen valant True si on souhaite obtenir des statistiques par codes résultat
        :param filtre_pot:
        l'identifiant, dans la base de données Agents, de l'agent dont on souhaite obtenir des statistiques sur son pot
        (c'est-à-dire sur sa liste de fiches adresse à contrôler/reprendre)
        :param filtre_lot:
        l'identifiant de lot, dans la base de données, des fiches adresse pour lesquelles on souhaite obtenir des statistiques
        :param filtre_code_resultat:
        le code résultat pour lequel on souhaite obtenir des statistiques
        :return:
        renvoie la liste de statistiques demandées en argument
        """
        if filtre_code_resultat is not None and filtre_code_resultat not in ["TF", "TA", "TH", "TC", "TR", "EF",
                                                                             "ER", "VA", "VC", "VR"]:
            raise ValueError("Impossible de filtrer sur un code résultat illégal.")
        res = self.__interface.obtenir_statistiques([par_pot, par_lot, par_code_resultat,
                                                     filtre_pot, filtre_lot, filtre_code_resultat])
        return res

    def recuperer_dernier_id_fa(self) -> int:
        """
        Cette méthode permet de récupérer le dernier identifiant de fiche adresse de la base de données FA,
        c'est-à-dire l'identifiant attribué en dernier à une fiche adresse dans la base de données FA.

        :return:
        renvoie le dernier identifiant de fiche adresse de la base de données FA
        """
        value = self.__interface.recuperer_dernier_id_fa()
        return value

    def recuperer_dernier_id_lot(self) -> int:
        """
        Cette méthode permet de récupérer le dernier identifiant de lot de la base de données FA,
        c'est-à-dire l'identifiant attribué en dernier dans la base de données FA à une liste de fiches adresse importées simultanément.

        :return:
        renvoie le dernier identifiant de lot de fiches adresse de la base de données FA
        """
        value = self.__interface.recuperer_dernier_id_lot()
        return value

    def incrementer_id_lot(self) -> bool:
        """
        Cette méthode permet d'incrément l'identifiant de lot,
        c'est-à-dire de comptabiliser une liste supplémentaire de fiches adresse importées simultanément dans l'application PSyCoQuAC. 

        :return:
        renvoie un booléen si l'identifiant de lot a été correctement incrémenté
        """
        res = self.__interface.incrementer_id_lot()
        return res
