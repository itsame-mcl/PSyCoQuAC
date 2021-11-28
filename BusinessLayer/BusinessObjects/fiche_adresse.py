from datetime import date
from BusinessLayer.BusinessObjects.adresse import Adresse
import attr


def _update_date_modification(instance, attribute, value):
    instance.date_modification = date.today()
    return value


def _validate_code_res(instance, attribute, value):
    if attribute.name == 'code_res':
        if instance.code_res != value:
            if instance.code_res == "TF":
                if value not in ["TA", "EF"]:
                    raise ValueError("La transition depuis l'état TF ne peut se faire que vers l'état TA ou l'état EF.")
            elif instance.code_res == "TA":
                if value not in ["TH", "TR"]:
                    raise ValueError("La transition depuis l'état TA ne peut se faire que vers l'état TH ou l'état TR.")
            elif instance.code_res == "TH":
                if value not in ["TC", "VA"]:
                    raise ValueError("La transition depuis l'état TH ne peut se faire que vers l'état TC ou l'état VA.")
            elif instance.code_res == "TC":
                if value not in ["TR", "VC"]:
                    raise ValueError("La transition depuis l'état TC ne peut se faire que vers l'état TR ou l'état VC.")
            elif instance.code_res == "TR":
                if value not in ["VR", "ER"]:
                    raise ValueError("La transition depuis l'état TR ne peut se faire que vers l'état VR ou l'état ER.")
            elif instance.code_res == "EF":
                raise ValueError("L'état EF est un état final.")
            elif instance.code_res == "ER":
                raise ValueError("L'état ER est un état final.")
            elif instance.code_res == "VA":
                raise ValueError("L'état VA est un état final.")
            elif instance.code_res == "VC":
                raise ValueError("L'état VC est un état final.")
            elif instance.code_res == "VR":
                raise ValueError("L'état VR est un état final.")
    else:
        raise AttributeError("Ce validateur ne s'applique qu'à l'attribue code_res.")
    return value


@attr.s
class FicheAdresse(object):
    """
       :param fiche_id:
       l'identifiant, dans la base de données FA, de la fiche adresse
       :param agent_id:
       l'identifiant, dans la base de données Agents, de l'agent en charge de la fiche adresse
       :param lot_id:
       l'identifiant du lot de la fiche adresse, c'est-à-dire l'identifiant du fichier contenant l'ensemble
       des fiches
       adresse qui ont été importées en même temps
       :param adresse_initiale:
       l'adresse contenue dans la fiche avant la géolocalisation par l'API
       :param adresse_finale:
       l'adresse contenue dans la fiche après la géolocalisation par l'API
       :param date_importation:
       la date d'importation de la fiche adresse dans l'application
       :param date_modification:
       la date de la dernière modification de la fiche adresse
       :param coords_wgs84:
       les coordonnées de l'adresse de la fiche selon le système géodésique WSG84 (coordonnées GPS)
       :param champs_supplementaires:
       une (ou plusieurs) information(s) supplémentaire(s) sur l'adresse de la fiche
       :param code_res:
       le code résultat de la fiche adresse, donnant son état :
           TF = une fiche adresse à filtrer par le service d'importation
           TA = une fiche adresse à traiter par l'API
           TH = une fiche adresse traitée par l'API à échantilloner
           TC = une fiche adresse à contrôler
           TR = une fiche adresse à reprendre
           EF = une fiche adresse considérée comme impossible à géolocaliser par l'API, selon le
           service d'importation
           ER = une fiche échec reprise (une fiche adresse dont les problèmes empêchant la géolocalisation n'ont pu
           être résolus)
           VA = une fiche adresse géolocalisée par l'API et n'ayant pas été échantilonnée
           VC = une fiche adresse dont le contrôle a confirmé que la géolocaliser était correcte
           VR = une fiche adresse dont la reprise à permis de la géolocaliser correctement
   """
    fiche_id: int = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)),
                            on_setattr=attr.setters.frozen)
    agent_id: int = attr.ib(converter=int, on_setattr=_update_date_modification)
    lot_id: int = attr.ib(converter=int, on_setattr=attr.setters.frozen)
    adresse_initiale: Adresse = attr.ib(validator=attr.validators.instance_of(Adresse),
                                        on_setattr=attr.setters.frozen)
    adresse_finale: Adresse = attr.ib(validator=attr.validators.instance_of(Adresse),
                                      on_setattr=_update_date_modification)
    @adresse_finale.default
    def _default_adresse_finale(self):
        return self.adresse_initiale

    date_importation: date = attr.ib(default=date.today(), validator=attr.validators.instance_of(date),
                                     on_setattr=attr.setters.frozen)
    date_modification: date = attr.ib(default=date.today(), validator=attr.validators.instance_of(date))
    coords_wgs84: tuple = attr.ib(factory=tuple, validator=attr.validators.instance_of(tuple),
                                  on_setattr=_update_date_modification)
    champs_supplementaires: dict = attr.ib(factory=dict, validator=attr.validators.instance_of(dict),
                                           on_setattr=_update_date_modification)
    code_res: str = attr.ib(default='TF', on_setattr=[_validate_code_res, _update_date_modification])
    @code_res.validator
    def _validator_code_res(self, attribute, value):
        if value not in ["TF", "TA", "TH", "TC", "TR", "EF", "ER", "VA", "VC", "VR"]:
            raise ValueError("Impossible d'initialiser un objet FicheAdresse avec un code résultat illégal.")

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

    def as_dict(self, expand: bool = False):
        """
        Cette méthode transforme la fiche adresse en dictionnaire,
        dont les valeurs sont les paramètres de la fiche adresse.

        :param expand:
        un booléen valant True si la fiche adresse contient plusieurs champs supplémentaires
        :return:
        renvoie un dictionnaire contenant les informations de la fiche adresse
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
