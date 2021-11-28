from typing import Tuple
from utils.converters import int_to_tuple
import attr


@attr.s
class Correspondance(object):
    """
         :param position_numero:
         la position dans le fichier de la colonne contenant le numéro des adresses dans le fichier
         :param position_voie:
         la position dans le fichier de la colonne contenant le type de voie
         (rue, impasse, avenue, boulevard) des adresses dans le fichier
         :param position_cp:
         la position dans le fichier de la colonne contenant le code postal des adresses dans le fichier
         :param position_ville:
         la position dans le fichier de la colonne contenant le nom de la ville des adresses
         :param positions_supplementaires:
         la position dans le fichier de la (ou les) colonne(s) contenant une
         information supplémentaire sur les adresses
     """
    position_numero: Tuple[int] = attr.ib(converter=int_to_tuple, validator=attr.validators.instance_of(tuple),
                                          on_setattr=attr.setters.convert)
    position_voie: Tuple[int] = attr.ib(converter=int_to_tuple, validator=attr.validators.instance_of(tuple),
                                        on_setattr=attr.setters.convert)
    position_cp: Tuple[int] = attr.ib(converter=int_to_tuple, validator=attr.validators.instance_of(tuple),
                                      on_setattr=attr.setters.convert)
    position_ville: Tuple[int] = attr.ib(converter=int_to_tuple, validator=attr.validators.instance_of(tuple),
                                         on_setattr=attr.setters.convert)
    positions_supplementaires: dict = attr.ib(factory=dict, validator=attr.validators.deep_mapping(
        key_validator=attr.validators.instance_of(str), value_validator=attr.validators.instance_of(int),
        mapping_validator=attr.validators.instance_of(dict)), on_setattr=attr.setters.validate)
