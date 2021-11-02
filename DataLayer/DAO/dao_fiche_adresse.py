import dotenv
from datetime import date

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
        adresse_initiale = Adresse(data["initial_numero"], data["initial_voie"], data["initial_code_postal"],
                                   data["initial_ville"])
        adresse_finale = Adresse(data["final_numero"], data["final_voie"], data["final_code_postal"],
                                 data["final_ville"])
        fa = FicheAdresse(data["identifiant_fa"], data["identifiant_pot"], data["identifiant_lot"], adresse_initiale,
                          adresse_finale, data["date_importation"], data["date_dernier_traitement"],
                          data["coordonnees_wgs84"], data["champs_supplementaires"],
                          data["code_resultat"])
        return fa

    def creer_fiche_adresse(self, fa: FicheAdresse) -> bool:
        res = self.__interface.creer_fiche_adresse(fa.as_dict())
        return res

    def modifier_fiche_adresse(self, fa: FicheAdresse) -> bool:
        res = self.__interface.modifier_fiche_adresse(fa.as_dict())
        return res

    def supprimer_fiche_adresse(self, identifiant: int) -> bool:
