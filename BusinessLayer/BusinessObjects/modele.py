from BusinessLayer.BusinessObjects.correspondance import Correspondance
import attr


@attr.s
class Modele(object):
    nom_modele: str = attr.ib(converter=str, on_setattr=attr.setters.convert)
    regex: str = attr.ib(converter=str, on_setattr=attr.setters.convert)
    correspondances: Correspondance = attr.ib(validator=attr.validators.instance_of(Correspondance))
    identifiant: int = attr.ib(default=None, converter=attr.converters.optional(int), on_setattr=attr.setters.frozen)

    @classmethod
    def from_dict(cls, data):
        correspondances = Correspondance(data["position_champ_numero"], data["position_champ_voie"],
                                         data["position_champ_code_postal"], data["position_champ_ville"],
                                         data["position_champs_supplementaires"])
        return cls(data["nom_modele"], data["regex_nom_fichier"], correspondances, data["identifiant_modele"])

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

    def __str__(self) -> str:
        chaine = "Modèle " + str(self.nom_modele) + "\n"
        chaine += "Expression régulière : " + str(self.regex) + "\n"
        numero = ', '.join([str(pos + 1) for pos in self.correspondances.position_numero])
        chaine += "Colonnes du numéro de l'habitation : " + numero + '\n'
        voie = ', '.join([str(pos + 1) for pos in self.correspondances.position_voie])
        chaine += "Colonnes du nom de la voie : " + voie + '\n'
        cp = ', '.join([str(pos + 1) for pos in self.correspondances.position_cp])
        chaine += "Colonnes du code postal : " + cp + '\n'
        ville = ', '.join([str(pos + 1) for pos in self.correspondances.position_ville])
        chaine += "Colonnes de la ville : " + ville + '\n'
        for champ, position in self.correspondances.positions_supplementaires.items():
            chaine += "Colonne de " + str(champ) + " : " + str(position+1) + '\n'
        return chaine
