from typing import Union, Tuple


class Correspondance:
    def __init__(self, position_numero: Union[int, Tuple[int]], position_voie: Union[int, Tuple[int]],
                 position_cp: Union[int, Tuple[int]], position_ville: Union[int, Tuple[int]],
                 positions_supplementaires: dict = None):
        """

        :param position_numero:
        la position dans le fichier de la colonne contenant le numéro des adresses dans le fichier
        :param position_voie:
        la position dans le fichier de la colonne contenant le type de voie (rue, impasse, avenue, boulevard) des adresses dans le fichier
        :param position_cp:
        la position dans le fichier de la colonne contenant le code postal des adresses dans le fichier
        :param position_ville:
        la position dans le fichier de la colonne contenant le nom de la ville des adresses
        :param positions_supplementaires:
        la position dans le fichier de la (ou les) colonne(s) contenant une information supplémentaire sur les adresses
        """
        if isinstance(position_numero, int):
            self._position_numero = (position_numero,)
        elif isinstance(position_numero, tuple):
            self._position_numero = position_numero
        else:
            raise TypeError
        if isinstance(position_voie, int):
            self._position_voie = (position_voie,)
        elif isinstance(position_voie, tuple):
            self._position_voie = position_voie
        else:
            raise TypeError
        if isinstance(position_cp, int):
            self._position_cp = (position_cp,)
        elif isinstance(position_cp, tuple):
            self._position_cp = position_cp
        else:
            raise TypeError
        if isinstance(position_ville, int):
            self._position_ville = (position_ville,)
        elif isinstance(position_ville, tuple):
            self._position_ville = position_ville
        else:
            raise TypeError
        if positions_supplementaires is None:
            self._positions_supplementaires = dict()
        elif isinstance(positions_supplementaires, dict):
            self._positions_supplementaires = positions_supplementaires
        else:
            raise TypeError

    @property
    def position_numero(self) -> tuple:
        return self._position_numero

    @position_numero.setter
    def position_numero(self, value: Union[int, Tuple[int]]):
        if isinstance(value, int):
            self._position_numero = (value,)
        elif isinstance(value, tuple):
            self._position_numero = value
        else:
            raise TypeError

    @property
    def position_voie(self) -> tuple:
        return self._position_voie

    @position_voie.setter
    def position_voie(self, value: Union[int, Tuple[int]]):
        if isinstance(value, int):
            self._position_voie = (value,)
        elif isinstance(value, tuple):
            self._position_voie = value
        else:
            raise TypeError

    @property
    def position_cp(self) -> tuple:
        return self._position_cp

    @position_cp.setter
    def position_cp(self, value: Union[int, Tuple[int]]):
        if isinstance(value, int):
            self._position_cp = (value,)
        elif isinstance(value, tuple):
            self._position_cp = value
        else:
            raise TypeError

    @property
    def position_ville(self) -> tuple:
        return self._position_ville

    @position_ville.setter
    def position_ville(self, value: Union[int, Tuple[int]]):
        if isinstance(value, int):
            self._position_ville = (value,)
        elif isinstance(value, tuple):
            self._position_ville = value
        else:
            raise TypeError

    @property
    def positions_supplementaires(self) -> dict:
        return self._positions_supplementaires

    @positions_supplementaires.setter
    def positions_supplementaires(self, value: dict):
        self._positions_supplementaires = value
