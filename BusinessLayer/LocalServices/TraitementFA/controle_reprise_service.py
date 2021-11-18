from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
from utils.singleton import Singleton
from typing import List


class ControleRepriseService(metaclass=Singleton):
    @staticmethod
    def consulter_fiche(id_fiche: int) -> FicheAdresse:
        return DAOFicheAdresse().recuperer_fiche_adresse(id_fiche)

    @staticmethod
    def modifier_fiche(id_fiche: int, nouvelles_informations: dict) -> bool:
        data = DAOFicheAdresse().recuperer_fiche_adresse(id_fiche).as_dict()
        if "identifiant_pot" in nouvelles_informations.keys:
            data["identifiant_pot"] = nouvelles_informations["identifiant_pot"]
        if "identifiant_lot" in nouvelles_informations.keys:
            data["identifiant_lot"] = nouvelles_informations["identifiant_lot"]
        if "code_resultat" in nouvelles_informations.keys:
            data["code_resultat"] = nouvelles_informations["code_resultat"]
        if "final_numero" in nouvelles_informations.keys:
            data["final_numero"] = nouvelles_informations["final_numero"]
        if "final_voie" in nouvelles_informations.keys:
            data["final_voie"] = nouvelles_informations["final_voie"]
        if "final_code_postal" in nouvelles_informations.keys:
            data["final_code_postal"] = nouvelles_informations["final_code_postal"]
        if "final_ville" in nouvelles_informations["final_ville"]:
            data["final_ville"] = nouvelles_informations["final_ville"]
        if "coordonnees_wgs84" in nouvelles_informations["coordonnees_wgs84"]:
            data["coordonnees_wgs84"] = nouvelles_informations["coordonnees_wgs84"]
        fa = FicheAdresse.from_dict(data)
        res = DAOFicheAdresse().modifier_fiche_adresse(fa)
        return res

    @staticmethod
    def consulter_pot(id_agent: int) -> List[FicheAdresse]:
        return DAOFicheAdresse().recuperer_pot(id_agent)
