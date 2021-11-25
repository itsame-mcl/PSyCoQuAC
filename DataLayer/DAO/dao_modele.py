from BusinessLayer.BusinessObjects.modele import Modele
import DataLayer.DAO.interface_factory as factory
from utils.singleton import Singleton


class DAOModele(metaclass=Singleton):
    def __init__(self):
        self.__interface = factory.InterfaceFactory.get_interface("Modele")

    def recuperer_modele(self, identifiant: int) -> Modele:
        """
        Cette méthode permet de récupérer le modèle de fichier à importer de la base de données Modeles,
        dont on a renseigné l'identifiant de la base de données Modeles.

        :param identifiant:
        l'identifiant, dans la base de données Modeles, du modèle que l'on cherche à récupérer
        :return:
        renvoie le Business Object Modele correspondant à l'identifiant passé en argument
        """
        data = self.__interface.recuperer_modele(identifiant)
        return Modele.from_dict(data)

    def recuperer_regex(self) -> dict:
        """
        Cette méthode permet de récupérer l'expression (ou les expressions) régulière(s).

        :return:
        renvoie un dictionnaire contenant l'expression (ou les expressions) régulière(s) récupérée(s)
        """
        data = self.__interface.recuperer_regex()
        return data

    def creer_modele(self, modele: Modele) -> bool:
        """
        Cette méthode permet de créer, dans la base de données Modeles, un modèle de fichier à importer,
        en renseignant la position des colonnes contenant les informations des adresses contenues dans le fichier.

        :param modele:
        les paramètres du modèle que l'on souhaite créer
        :return:
        renvoie un booléen valant True si le modèle a été correctement créé
        """
        res = self.__interface.creer_modele(modele.as_dict())
        return res

    def modifier_modele(self, modele: Modele) -> bool:
        """
        Cette méthode permet de modifier les informations contenant dans un modèle de fichier à importer de la base de données Modeles.

        :param modele:
        le modèle que l'on cherche à modifier dans la base de données Modeles
        :return:
        renvoie un booléen valant True si le a été correctement modifié dans la base de données Modeles
        """
        res = self.__interface.modifier_modele(modele.as_dict())
        return res

    def supprimer_modele(self, identifiant: int) -> bool:
        """
        Cette méthode permet de supprimer un modèle de fichier à importer de la base de données Modeles.

        :param identifiant:
        l'identifiant, dans la base de données Modeles, du modèle que l'on cherche supprimer de la base de données Modeles
        :return:
        renvoie un booléen valant True si le modèle a été correctement supprimé de la base de données Modeles
        """
        res = self.__interface.supprimer_modele(identifiant)
        return res

    def recuperer_dernier_id_modele(self) -> int:
        """
        Cette méthode permet de récupérer le dernier identifiant de modèle de fichier à importer de la base de données Modeles,
        c'est-à-dire l'identifiant attribué en dernier dans la base de données Modeles à un modèle de fichier à importer.

        :return:
        renvoie le dernier identifiant de modèle de la base de données Modeles
        """
        value = self.__interface.recuperer_dernier_id_modele()
        return value
