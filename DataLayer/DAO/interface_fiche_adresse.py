from abc import ABC, abstractmethod
from typing import List


class InterfaceFicheAdresse(ABC):

    @abstractmethod
    def recuperer_fiche_adresse(self, identifiant: int) -> dict:
        raise NotImplementedError

    @abstractmethod
    def recuperer_liste_fiches_adresse(self, id_agent: int, id_lot: int) -> List[dict]:
        raise NotImplementedError

    @abstractmethod
    def creer_fiche_adresse(self, data: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def creer_multiple_fiche_adresse(self, data: List[dict]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def modifier_fiche_adresse(self, data: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def modifier_multiple_fiche_adresse(self, data: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def modifier_agent_fiches_adresse(self, id_agent: int, code_res: str, id_fas: List[int]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def supprimer_fiche_adresse(self, identifiant: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def obtenir_statistiques(self, champs: list) -> List[tuple]:
        raise NotImplementedError

    @staticmethod
    def _obtenir_statistiques_request_helper(criteria: list) -> str:
        fields = []
        filters = []
        if criteria[0]:
            fields.append('identifiant_pot')
        if criteria[1]:
            fields.append('identifiant_lot')
        if criteria[2]:
            fields.append('code_resultat')
        fields.append("COUNT(identifiant_fa)")
        if criteria[3] is not None:
            filters.append('identifiant_pot=' + str(int(criteria[3])))
        if criteria[4] is not None:
            filters.append('identifiant_lot=' + str(int(criteria[4])))
        if criteria[5] is not None:
            if criteria[5] in ["TF", "TA", "TH", "TC", "TR", "EF", "ER", "VA", "VC", "VR"]:  # sécurité anti_injection
                filters.append('code_resultat=' + '"' + criteria[5] + '"')
        request = "SELECT " + str(fields).strip('[]').replace("'", "") + " FROM fa"
        if len(filters) > 0:
            request = request + " WHERE " + \
                      str(filters).strip('[]').replace("'", "").replace('"', "'").replace(",", " AND")
        fields.remove("COUNT(identifiant_fa)")
        if len(fields) > 0:
            request = request + " GROUP BY " + str(fields).strip('[]').replace("'", "")
        return request

    @abstractmethod
    def recuperer_dernier_id_fa(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def recuperer_dernier_id_lot(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def incrementer_id_lot(self) -> bool:
        raise NotImplementedError
