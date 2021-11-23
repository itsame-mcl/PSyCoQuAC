from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
from utils.singleton import Singleton
from typing import List


class ControleRepriseService(metaclass=Singleton):
    @staticmethod
    def consulter_fiche(id_fiche: int) -> FicheAdresse:
        """

        :param id_fiche:
        :return:
        """
        return DAOFicheAdresse().recuperer_fiche_adresse(id_fiche)

    @staticmethod
    def modifier_fiche(fiche_modifiee: FicheAdresse) -> bool:
        """

        :param fiche_modifiee:
        :return:
        """
        res = DAOFicheAdresse().modifier_fiche_adresse(fiche_modifiee)
        return res

    @staticmethod
    def validation_fiche(fiche: FicheAdresse, validation: bool) -> bool:
        """

        :param fiche:
        :param validation:
        :return:
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

        :param id_agent:
        :return:
        """
        return DAOFicheAdresse().recuperer_pot(id_agent)

    @staticmethod
    def consulter_pot_controle_reprise(id_agent: int, controle=True, reprise=True) -> List[FicheAdresse]:
        """

        :param id_agent:
        :param controle:
        :param reprise:
        :return:
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
