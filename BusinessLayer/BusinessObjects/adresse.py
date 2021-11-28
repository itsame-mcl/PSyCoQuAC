import attr


@attr.s
class Adresse(object):
    """
        :param numero:
        le numéro de l'adresse
        :param voie:
        le type de voie (rue, impasse, avenue, boulevard) de l'adresse
        :param cp:
        le code postal de l'adresse
        :param ville:
        le nom de la ville de l'adresse
    """
    numero: str = attr.ib(converter=attr.converters.optional(str), on_setattr=attr.setters.convert)
    voie: str = attr.ib(converter=attr.converters.optional(str), on_setattr=attr.setters.convert)
    cp: str = attr.ib(converter=attr.converters.optional(str), on_setattr=attr.setters.convert)
    ville: str = attr.ib(converter=attr.converters.optional(str), on_setattr=attr.setters.convert)

    def __str__(self):
        res = str(self.numero) + " " + str(self.voie) + " " + str(self.cp) + " " + str(self.ville)
        return res
