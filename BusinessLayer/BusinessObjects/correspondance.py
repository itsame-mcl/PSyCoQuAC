class Correspondance:

    def __init__(self, position_numero: int, position_voie: int, position_cp: int, position_ville: int,
                 positions_supplementaires: dict = None):
        self._position_numero = position_numero
        self._position_voie = position_voie
        self._position_cp = position_cp
        self._position_ville = position_ville
        if positions_supplementaires is None:
            self._positions_supplementaires = dict()
        else:
            self._positions_supplementaires = positions_supplementaires

    @property
    def position_numero(self) -> int:
        return self._position_numero

    @position_numero.setter
    def position_numero(self, value: int):
        self._position_numero = value

    @property
    def position_voie(self) -> int:
        return self._position_voie

    @position_voie.setter
    def position_voie(self, value: int):
        self._position_voie = value

    @property
    def position_cp(self) -> int:
        return self._position_cp

    @position_cp.setter
    def position_cp(self, value: int):
        self._position_cp = value

    @property
    def position_ville(self) -> int:
        return self._position_ville

    @position_ville.setter
    def position_ville(self, value: int):
        self._position_ville = value

    @property
    def positions_supplementaires(self) -> dict:
        return self._positions_supplementaires

    @positions_supplementaires.setter
    def positions_supplementaires(self, value: dict):
        self._positions_supplementaires = value
