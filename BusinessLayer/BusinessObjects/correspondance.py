class Correspondance:
    def __init__(self, position_numero : int, position_voie : int, position_cp : int, position_ville : int,
                 positions_supplementaires : dict = None):
        self._position_numero = position_numero
        self._position_voie = position_voie
        self._position_ville = position_ville
        if positions_supplementaires is None:
            self._positions_supplementaires = dict()
        else:
            self._positions_supplementaires = positions_supplementaires