from BusinessLayer.BusinessObjects.correspondance import Correspondance


class Modele:
    def __init__(self, nom_modele: str, regex_nom_fichier: str,
                 correspondances: Correspondance, identifiant: int = None):
        self._identifiant: int = identifiant
        self._nom_modele: str = nom_modele
        self._regex: str = regex_nom_fichier
        self._correspondances: Correspondance = correspondances

    @classmethod
    def from_dict(cls, data):
        correspondances = Correspondance(data["position_champ_numero"], data["position_champ_voie"],
                                         data["position_champ_code_postal"], data["position_champ_ville"],
                                         data["position_champs_supplementaires"])
        return cls(data["nom_modele"], data["regex_nom_fichier"], correspondances, data["identifiant_modele"])

    @property
    def identifiant(self) -> int:
        return self._identifiant

    @property
    def nom_modele(self) -> str:
        return self._nom_modele

    @nom_modele.setter
    def nom_modele(self, value: str):
        self._nom_modele = value

    @property
    def regex(self) -> str:
        return self._regex

    @regex.setter
    def regex(self, value: str):
        self._regex = value

    @property
    def correspondances(self) -> Correspondance:
        return self._correspondances

    @correspondances.setter
    def correspondances(self, value: Correspondance):
        self._correspondances = value

    def as_dict(self) -> dict:
        data = dict()
        data["identifiant_modele"] = self.identifiant
        data["nom_modele"] = self.nom_modele
        data["regex_nom_fichier"] = self.regex
        data["position_champ_numero"] = self.correspondances.position_numero
        data["position_champ_voie"] = self.correspondances.position_voie
        data["position_champ_code_postal"] = self.correspondances.position_cp
        data["position_champ_ville"] = self.correspondances.position_ville
        data["position_champs_supplementaires"] = self.correspondances.positions_supplementaires
        return data
