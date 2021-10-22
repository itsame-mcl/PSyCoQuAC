class FicheAdresse:
    def __init__(self, fiche_id, agent_id, lot_id, adresse_initiale, adresse_finale=None, coords_WGS84=None, champs_supplementaires=None, code_res="TI"):
        self._fiche_id = fiche_id
        self._agent_id = agent_id
        self._lot_id = lot_id
        if code_res in ["TI","TA","TH","TC","TR","DI","ER","VA","VC","VR"]:
            self._code_res = code_res
        else:
            raise ValueError("Impossible d'initialiser un objet FicheAdresse avec un code résultat illégal.")
        self._adresse_initiale = adresse_initiale
        if adresse_finale is None:
            self._adresse_finale = adresse_initiale
        else:
            self._adresse_finale = adresse_finale
        if coords_WGS84 is None:
            self.coords_WGS84 = dict()
        else:
            self._coords_WGS84 = coords_WGS84
        if champs_supplementaires is None:
            self._champs_suplementaires = dict()
        else:
            self._champs_suplementaires = champs_supplementaires
    
    @property
    def fiche_id(self):
        return self._fiche_id
    
    @property
    def agent_id(self):
        return self._agent_id
    
    @agent_id.setter
    def agent_id(self, value):
        self._agent_id = value
    
    @property
    def lot_id(self):
        return self._lot_id
    
    @property
    def code_res(self):
        return self._code_res
    
    @property.setter
    def code_res(self, value):
        if self._code_res == "TI":
            if value in ["TA","DI"]:
                self._code_res = value
            else:
                raise ValueError("La transition depuis l'état TI ne peut se faire que vers l'état TA ou l'état DI.")
        elif self._code_res == "TA":
            if value in ["TH","TR"]:
                self._code_res = value
            else:
                raise ValueError("La transition depuis l'état TA ne peut se faire que vers l'état TH ou l'état TR.")
        elif self._code_res == "TH":
            if value in ["TC","VA"]:
                self._code_res = value
            else:
                raise ValueError("La transition depuis l'état TH ne peut se faire que vers l'état TC ou l'état VA.")
        elif self._code_res == "TC":
            if value in ["TR","VC"]:
                self._code_res = value
            else:
                raise ValueError("La transition depuis l'état TC ne peut se faire que vers l'état TR ou l'état VC.")
        elif self._code_res == "TR":
            if value in ["VR","ER"]:
                self._code_res = value
            else:
                raise ValueError("La transition depuis l'état TR ne peut se faire que vers l'état VR ou l'état ER.")
        elif self._code_res == "DI":
            raise ValueError("L'état DI est un état final.")
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
    
    @property
    def coords_WGS84(self):
        return self._coords_WGS84
    
    @coords_WGS84.setter
    def coords_WGS84(self, value):
        self._coords_WGS84 = value
    
    @property
    def champs_supplementaires(self):
        return self._champs_suplementaires
    
    @champs_supplementaires.setter
    def champs_supplementaires(self, value):
        self._champs_suplementaires = value
