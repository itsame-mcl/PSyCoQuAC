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

    def recuperer_fiche_adresse(self, identifiant : int) -> FicheAdresse:
        data = self.__interface.recuperer_fiche_adresse(identifiant)
        adresse_initiale = Adresse(data["initial_numero"], data["initial_voie"], data["initial_code_postal"],
                                   data["initial_ville"])
        adresse_finale = Adresse(data["final_numero"], data["final_voie"], data["final_code_postal"],
                                 data["final_ville"])
        fa = FicheAdresse(data["identifiant_fa"], data["identifiant_pot"], data["identifiant_lot"], adresse_initiale,
                          adresse_finale, data["coordonnees_wgs84"], data["champs_supplementaires"],
                          data["code_resultat"])
        return fa

    def creer_fiche_adresse(self, fa : FicheAdresse) -> bool:
        data = dict()
        data["identifiant_pot"] = fa.agent_id
        data["identifiant_lot"] = fa.lot_id
        data["code_resultat"] = fa.code_res
        data["date_importation"] = date.today()
        data["date_dernier_traitement"] = date.today()
        data["initial_numero"] = fa.adresse_initiale.numero
        data["initial_voie"] = fa.adresse_initiale.voie
        data["initial_code_postal"] = fa.adresse_initiale.cp
        data["initial_ville"] = fa.adresse_initiale.ville
        data["final_numero"] = fa.adresse_finale.numero
        data["final_voie"] = fa.adresse_finale.voie
        data["final_code_postal"] = fa.adresse_finale.cp
        data["final_ville"] = fa.adresse_finale.ville
        data["coordonnees_wgs84"] = fa.coords_wgs84
        data["champs_supplementaires"] = fa.champs_supplementaires
        res = self.__interface.creer_fiche_adresse(data)
        return res
