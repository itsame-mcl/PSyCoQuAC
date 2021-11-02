import dotenv

from BusinessLayer.BusinessObjects.adresse import Adresse
from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from DataLayer.DAO.sqlite_fiche_adresse import SQLiteFicheAdresse
from utils.singleton import Singleton


class DAOFicheAdresse(metaclass=Singleton):
    def __init__(self):
        engine = dotenv.dotenv_values(".env")["ENGINE"]
        if engine == "SQLite":
            self.__interface = SQLiteFicheAdresse()

    def recuperer_fiche_adresse(self, identifiant: int) -> FicheAdresse:
        data = self.__interface.recuperer_fiche_adresse(identifiant)
        return FicheAdresse.from_dict(data)

    def creer_fiche_adresse(self, fa: FicheAdresse) -> bool:
        res = self.__interface.creer_fiche_adresse(fa.as_dict())
        return res

    def modifier_fiche_adresse(self, fa: FicheAdresse) -> bool:
        res = self.__interface.modifier_fiche_adresse(fa.as_dict())
        return res

    def supprimer_fiche_adresse(self, identifiant: int) -> bool:
        res = self.__interface.supprimer_fiche_adresse(identifiant)
        return res
