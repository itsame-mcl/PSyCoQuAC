from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
from utils.singleton import Singleton
from typing import List


class ControleRepriseService(metaclass=Singleton):
    @staticmethod
    def consulter_fiche(id_fiche: int) -> FicheAdresse:
        return DAOFicheAdresse().recuperer_fiche_adresse(id_fiche)

    @staticmethod
    def modifier_fiche(fiche_modifiee: FicheAdresse) -> bool:
        res = DAOFicheAdresse().modifier_fiche_adresse(fiche_modifiee)
        return res

    def validation_fiche(self, fiche: FicheAdresse, validation: bool) -> bool:
        if validation:
            fiche.code_res = "VC"
        else:
            fiche.code_res = "TR"
        res = DAOFicheAdresse().modifier_fiche_adresse(fiche)
        if not res:
            print("La sauvegarde du contrôle a échoué. Veuillez réessayer ultérieurement.")
        return res

    @staticmethod
    def consulter_pot(id_agent: int) -> List[FicheAdresse]:
        return DAOFicheAdresse().recuperer_pot(id_agent)
