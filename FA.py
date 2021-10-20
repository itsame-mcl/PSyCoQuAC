class FicheAdresse:
    def __init__(self, fiche_id, agent_id, lot_id, code_res, adresse_initiale, adresse_finale, coords_WGS84, champs_supplementaires):
        self._fiche_id = fiche_id
        self._agent_id = agent_id
        self._lot_id = lot_id 
        self._code_res = code_res
        self._adresse_initiale = adresse_initiale
        self._adresse_finale = adresse_finale
        self._coords_WGS84 = coords_WGS84
        self._champs_suplementaires = champs_supplementaires
    
    @property
    def fiche_id(self):
        return self._fiche_id
    
    @property
    def agent_id(self):
        return self._agent_id
    
    @agent_id.setter
    def agent_id(self, value):
        #ajouter condition ? seulement superviseur ?
        self._agent_id = value
    
    @property
    def lot_id(self):
        return self._lot_id
    
    @property
    def code_res(self):
        return self._code_res
    
    @property
    def adresse_initiale(self):
        return self._adresse_initiale
    
    @property
    def adresse_finale(self):
        return self._adresse_finale
    
    @adresse_finale.setter
    def adresse_finale(self, value):
        #ajouter condition ?
        self._adresse_finale = value
    
    @property
    def coords_WGS84(self):
        return self._coords_WGS84
    
    @coords_WGS84.setter
    def coords_WGS84(self, value):
        #ajouter condition ?
        self._coords_WGS84 = value
    
    @property
    def champs_supplementaires(self):
        return self._champs_suplementaires
    
    @champs_supplementaires.setter
    def champs_supplementaires(self, value):
        #ajouter condition ?
        self._champs_suplementaires = value
    
    def modifier_code_res(self, new_code):
        self._code_res = new_code