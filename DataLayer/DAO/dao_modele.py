from BusinessLayer.BusinessObjects.modele import Modele
import DataLayer.DAO.interface_factory as factory
from utils.singleton import Singleton


class DAOModele(metaclass=Singleton):
    def __init__(self):
        self.__interface = factory.InterfaceFactory.get_interface("Agent")

    def recuperer_modele(self, identifiant: int) -> Modele:
        data = self.__interface.recuperer_modele(identifiant)
        return Modele.from_dict(data)

    def recuperer_regex(self) -> dict:
        data = self.__interface.recuperer_regex()
        return data

    def creer_modele(self, modele: Modele) -> bool:
        res = self.__interface.creer_modele(modele.as_dict())
        return res

    def modifier_modele(self, modele: Modele) -> bool:
        res = self.__interface.modifier_modele(modele.as_dict())
        return res

    def supprimer_modele(self, identifiant: int) -> bool:
        res = self.__interface.supprimer_modele(identifiant)
        return res

    def recuperer_dernier_id_modele(self) -> int:
        value = self.__interface.recuperer_dernier_id_modele()
        return value
