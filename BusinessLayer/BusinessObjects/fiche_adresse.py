from datetime import date
from BusinessLayer.BusinessObjects.adresse import Adresse


class FicheAdresse:
    def __init__(self, fiche_id: int, agent_id: int, lot_id: int, adresse_initiale: Adresse,
                 adresse_finale: Adresse = None, date_importation: date = date.today(),
                 date_modification: date = date.today(), coords_wgs84: dict = None,
                 champs_supplementaires: dict = None, code_res: str = "TI"):
        """

        :param fiche_id:
        l'identifiant, dans la base de données FA, de la fiche adresse
        :param agent_id:
        l'identifiant, dans la base de données Agents, de l'agent en charge de la fiche adresse
        :param lot_id:
        l'identifiant du lot de la fiche adresse, c'est-à-dire l'identifiant du fichier contenant l'ensemble des fiches adresse qui ont été importées en même temps
        :param adresse_initiale:
        l'adresse
        :param adresse_finale:
        :param date_importation:
        la date d'importation de la fiche adresse dans l'application
        :param date_modification:
        :param coords_wgs84:
        :param champs_supplementaires:
        :param code_res:
        le code résultat de la fiche adresse, donnant son état :
            TF = une fiche adresse à filtrer par le service d'importation  
            TA = une fiche adresse à traiter par l'API
            TH = une fiche adresse traitée par l'API à échantilloner
            TC = une fiche adresse à contrôler
            TR = une fiche adresse à reprendre
            DF = une fiche adresse considérée comme impossible à géolocaliser par l'API, selon le service d'importation
            ER = une fiche échec reprise (une fiche adresse dont les problèmes empêchant la géolocalisation n'ont pu être résolus )
            VA = une fiche adresse géolocalisée par l'API et n'ayant pas été échantilonnée
            VC = une fiche adresse dont le contrôle a confirmé que la géolocaliser était correcte
            VR = une fiche adresse dont la reprise à permis de la géolocaliser correctement
        """
        self._fiche_id = fiche_id
        self._agent_id = agent_id
        self._lot_id = lot_id
        self._date_importation = date_importation
        self._date_modification = date_modification
        if code_res in ["TF", "TA", "TH", "TC", "TR", "DF", "ER", "VA", "VC", "VR"]:
            self._code_res = code_res
        else:
            raise ValueError("Impossible d'initialiser un objet FicheAdresse avec un code résultat illégal.")
        self._adresse_initiale = adresse_initiale
        if adresse_finale is None:
            self._adresse_finale = adresse_initiale
        else:
            self._adresse_finale = adresse_finale
        if coords_wgs84 is None:
            self.coords_wgs84 = dict()
        else:
            self._coords_wgs84 = coords_wgs84
        if champs_supplementaires is None:
            self._champs_supplementaires = dict()
        else:
            self._champs_supplementaires = champs_supplementaires

    @classmethod
    def from_dict(cls, data):
        adresse_initiale = Adresse(data["initial_numero"], data["initial_voie"], data["initial_code_postal"],
                                   data["initial_ville"])
        adresse_finale = Adresse(data["final_numero"], data["final_voie"], data["final_code_postal"],
                                 data["final_ville"])
        return cls(data["identifiant_fa"], data["identifiant_pot"], data["identifiant_lot"], adresse_initiale,
                   adresse_finale, data["date_importation"], data["date_dernier_traitement"],
                   data["coordonnees_wgs84"], data["champs_supplementaires"],
                   data["code_resultat"])

    @property
    def fiche_id(self):
        return self._fiche_id

    @property
    def agent_id(self):
        return self._agent_id

    @agent_id.setter
    def agent_id(self, value):
        self._agent_id = value
        self._date_modification = date.today()

    @property
    def lot_id(self):
        return self._lot_id

    @property
    def date_importation(self):
        return self._date_importation

    @property
    def date_modification(self):
        return self._date_modification

    @date_modification.setter
    def date_modification(self, value):
        self.date_modification = value

    @property
    def code_res(self):
        return self._code_res

    @code_res.setter
    def code_res(self, value):
        """

        :param value:
        """
        if self._code_res == "TF":
            if value in ["TA", "DF"]:
                self._code_res = value
                self._date_modification = date.today()
            else:
                raise ValueError("La transition depuis l'état TI ne peut se faire que vers l'état TA ou l'état DI.")
        elif self._code_res == "TA":
            if value in ["TH", "TR"]:
                self._code_res = value
                self._date_modification = date.today()
            else:
                raise ValueError("La transition depuis l'état TA ne peut se faire que vers l'état TH ou l'état TR.")
        elif self._code_res == "TH":
            if value in ["TC", "VA"]:
                self._code_res = value
                self._date_modification = date.today()
            else:
                raise ValueError("La transition depuis l'état TH ne peut se faire que vers l'état TC ou l'état VA.")
        elif self._code_res == "TC":
            if value in ["TR", "VC"]:
                self._code_res = value
                self._date_modification = date.today()
            else:
                raise ValueError("La transition depuis l'état TC ne peut se faire que vers l'état TR ou l'état VC.")
        elif self._code_res == "TR":
            if value in ["VR", "ER"]:
                self._code_res = value
                self._date_modification = date.today()
            else:
                raise ValueError("La transition depuis l'état TR ne peut se faire que vers l'état VR ou l'état ER.")
        elif self._code_res == "DF":
            raise ValueError("L'état DF est un état final.")
        elif self._code_res == "ER":
            raise ValueError("L'état ER est un état final.")
        elif self._code_res == "VA":
            raise ValueError("L'état VA est un état final.")
        elif self._code_res == "VC":
            raise ValueError("L'état VC est un état final.")
        elif self._code_res == "VR":
            raise ValueError("L'état VR est un état final.")

    @property
    def adresse_initiale(self):
        return self._adresse_initiale

    @property
    def adresse_finale(self):
        return self._adresse_finale

    @adresse_finale.setter
    def adresse_finale(self, value):
        self._adresse_finale = value
        self._date_modification = date.today()

    @property
    def coords_wgs84(self):
        return self._coords_wgs84

    @coords_wgs84.setter
    def coords_wgs84(self, value):
        self._coords_wgs84 = value
        self._date_modification = date.today()

    @property
    def champs_supplementaires(self):
        return self._champs_supplementaires

    @champs_supplementaires.setter
    def champs_supplementaires(self, value):
        self._champs_supplementaires = value
        self._date_modification = date.today()

    def as_dict(self, expand: bool = False):
        """

        :param expand:
        :return:
        """
        data = dict()
        data["identifiant_fa"] = self.fiche_id
        data["identifiant_pot"] = self.agent_id
        data["identifiant_lot"] = self.lot_id
        data["code_resultat"] = self.code_res
        data["date_importation"] = self.date_importation
        data["date_dernier_traitement"] = self.date_modification
        data["initial_numero"] = self.adresse_initiale.numero
        data["initial_voie"] = self.adresse_initiale.voie
        data["initial_code_postal"] = self.adresse_initiale.cp
        data["initial_ville"] = self.adresse_initiale.ville
        data["final_numero"] = self.adresse_finale.numero
        data["final_voie"] = self.adresse_finale.voie
        data["final_code_postal"] = self.adresse_finale.cp
        data["final_ville"] = self.adresse_finale.ville
        data["coordonnees_wgs84"] = self.coords_wgs84
        if expand:
            for key, value in self.champs_supplementaires.items():
                data[key] = value
        else:
            data["champs_supplementaires"] = self.champs_supplementaires
        return data

    def __str__(self) -> str:
        chaine = "Fiche adresse n°" + str(self.fiche_id) + " - Lot n°" + str(self.lot_id) + "\n"
        chaine += "Etat actuel : " + str(self.code_res) + "\n"
        chaine += "Adresse initiale : " + str(self.adresse_initiale) + "\n"
        chaine += "Adresse finale : " + str(self.adresse_finale) + "\n"
        chaine += "Coordonnées WGS84 (GPS) : " + str(self.coords_wgs84)
        return chaine
