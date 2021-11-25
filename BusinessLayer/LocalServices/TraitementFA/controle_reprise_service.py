from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
from utils.singleton import Singleton
from typing import List


class ControleRepriseService(metaclass=Singleton):
    @staticmethod
    def consulter_fiche(id_fiche: int) -> FicheAdresse:
        """
        Cette méthode permet d'afficher les informations d'une fiche adresse.

        :param id_fiche:
        l'identifiant, dans la base de données FA, de la fiche adresse que l'on souhaite consulter
        :return:
        renvoie la fiche adresse que l'on souhaite consulter
        """
        return DAOFicheAdresse().recuperer_fiche_adresse(id_fiche)

    @staticmethod
    def modifier_fiche(fiche_modifiee: FicheAdresse) -> bool:
        """
        Cette méthode permet de modifier les informations d'une fiche adresse.

        :param fiche_modifiee:
        le Business Object FicheAdresse dont on cherche à modifier les informations
        :return:
        renvoie un booléen valant True si la fiche adresse a été correctement modifiée
        """
        res = DAOFicheAdresse().modifier_fiche_adresse(fiche_modifiee)
        return res

    @staticmethod
    def validation_fiche(fiche: FicheAdresse, validation: bool) -> bool:
        """
        Cette méthode permet de valider une fiche adresse contrôlée ou reprise.
        L'agent qui la contrôle peut décider que l'API a correctement traité la fiche adresse, et la valide.
        Si l'agent décide que l'API n'a pas correctement traité la fiche adresse, cette dernière doit alors être reprise.
        L'agent qui reprend la fiche adresse peut valider la modification opérée.
        Si l'agent décide que même la reprise ne permet pas d'obtenir une fiche adresse correcte, 
        cette dernière est considéré comme un échec de la reprise.
        Ces changements (fiche adresse validée, échec, à traiter par une reprise) sont opérés au travers du code résultat de la fiche adresse.

        :param fiche:
        le Business Object FicheAdresse à valider
        :param validation:
        un booléen valant True si l'agent qui contrôle/reprend la fiche adresse valide les informations de cette dernière.
        :return:
        renvoie un booléen si la fiche adresse a été correctement validée
        """
        if fiche.code_res == "TC":
            if validation:
                fiche.code_res = "VC"
            else:
                fiche.code_res = "TR"
        elif fiche.code_res == "TR":
            if validation:
                fiche.code_res = "VR"
            else:
                fiche.code_res = "ER"
        res = DAOFicheAdresse().modifier_fiche_adresse(fiche)
        if not res:
            print("La sauvegarde a échoué. Veuillez réessayer ultérieurement.")
        return res

    @staticmethod
    def consulter_pot(id_agent: int) -> List[FicheAdresse]:
        """
        Cette méthode permet d'afficher les fiches adresse qu'un agent,
        dont on renseigne l'identifiant de la base de données Agents, doit contrôler/reprendre.

        :param id_agent:
        l'identifiant, dans la base de données Agents, de l'agent dont on souhaite consulter le pot.
        :return:
        renvoie la liste de fiches adresse que l'agent doit contrôler/reprendre
        """
        return DAOFicheAdresse().recuperer_pot(id_agent)

    @staticmethod
    def consulter_pot_controle_reprise(id_agent: int, controle=True, reprise=True) -> List[FicheAdresse]:
        """
        Cette méthode permet d'afficher les fiches adresse qu'un agent,
        dont on renseigne l'identifiant de la base de données Agents, doit contrôler/reprendre.
        Cette méthode, avec les booléens controle et reprise, permet de choisir si on souhaite voir l'ensemble du pot de l'agent,
        seulement les fiches que l'agent doit controler, ou seulement les fiches que l'agent doit reprendre.

        :param id_agent:
        l'identifiant, dans la base de données Agents, de l'agent dont on souhaite consulter le pot.
        :param controle:
        un booléen valant True si on souhaite consulter la liste de fiches adresse que l'agent doit contrôler
        :param reprise:
        un booléen valant True si on souhaite consulter la liste de fiches adresse que l'agent doit reprendre
        :return:
        renvoie la liste de fiches adresse que l'agent doit contrôler/reprendre
        """
        pot = DAOFicheAdresse().recuperer_pot(id_agent)
        pot_cr = list()
        for fiche in pot:
            if controle:
                if fiche.code_res == "TC":
                    pot_cr.append(fiche)
            if reprise:
                if fiche.code_res == "TR":
                    pot_cr.append(fiche)
        return pot_cr
