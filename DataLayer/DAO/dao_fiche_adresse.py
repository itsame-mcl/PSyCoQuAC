from typing import List

from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
import DataLayer.DAO.interface_factory as factory
from utils.singleton import Singleton


class DAOFicheAdresse(metaclass=Singleton):
    def __init__(self):
        self.__interface = factory.InterfaceFactory.get_interface("FicheAdresse")

    def recuperer_fiche_adresse(self, identifiant: int) -> FicheAdresse:
        data = self.__interface.recuperer_fiche_adresse(identifiant)
        return FicheAdresse.from_dict(data)

    def recuperer_pot(self, identifiant: int) -> List[FicheAdresse]:
        data = self.__interface.recuperer_liste_fiches_adresse(identifiant, -1)
        pot = list()
        for row in data:
            pot.append(FicheAdresse.from_dict(row))
        return pot

    def recuperer_lot(self, identifiant: int) -> List[FicheAdresse]:
        data = self.__interface.recuperer_liste_fiches_adresse(-1, identifiant)
        lot = list()
        for row in data:
            lot.append(FicheAdresse.from_dict(row))
        return lot

    def affecter_fiches_adresse(self, identifiant_agent: int, liste_fiches_id: List[int]):
        res = self.__interface.modifier_agent_fiches_adresse(identifiant_agent, liste_fiches_id)
        return res

    def creer_fiche_adresse(self, fa: FicheAdresse) -> bool:
        res = self.__interface.creer_fiche_adresse(fa.as_dict())
        return res

    def modifier_fiche_adresse(self, fa: FicheAdresse) -> bool:
        res = self.__interface.modifier_fiche_adresse(fa.as_dict())
        return res

    def supprimer_fiche_adresse(self, identifiant: int) -> bool:
        res = self.__interface.supprimer_fiche_adresse(identifiant)
        return res

    def obtenir_statistiques(self, par_pot: bool = False, par_lot: bool = False, par_code_resultat: bool = False,
                             filtre_pot: int = None, filtre_lot: int = None,
                             filtre_code_resultat: str = None) -> List[tuple]:
            res = self.__interface.obtenir_statistiques([par_pot, par_lot, par_code_resultat,
                                                         filtre_pot, filtre_lot, filtre_code_resultat])
            return res

    def recuperer_prochain_id_lot(self):
        raise NotImplementedError
