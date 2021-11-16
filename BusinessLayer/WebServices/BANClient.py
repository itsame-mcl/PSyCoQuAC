from typing import List, Tuple
import requests
from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse


class BANClient:
    
    def geocodage_par_fiche(self, fiche_a_traiter : FicheAdresse) -> Tuple[float, FicheAdresse] :
        adresse = fiche_a_traiter.adresse_initiale
        adresse = adresse.replace(" ", "+")
        response = requests.get("https://api-adresse.data.gouv.fr/search/?q=" + str(adresse))
        response = response.json()
        score = response["score"]
        coordonnees_gps = response["coordinates"]
        fiche_a_traiter.coords_WGS84 = coordonnees_gps
        numero_rue = response["name"]
        code_postale = response["postcode"]
        adresse_API = numero_rue + code_postale
        fiche_a_traiter.adresse_finale = adresse_API
        return(score, fiche_a_traiter)
    
    def reverse_par_fiche(self, fiche_a_traiter : FicheAdresse) -> Tuple[float, FicheAdresse] :
        if len(fiche_a_traiter.coords_WGS84) == 0 :
            raise ValueError('La FicheAdresse ne possède pas de coordonnées GPS')
        coordonnees_gps = fiche_a_traiter.coords_WGS84
        lon=coordonnees_gps[0]
        lat=coordonnees_gps[1]
        response = requests.get("https://api-adresse.data.gouv.fr/reverse/?lon=" + str(lon) + "&lat=" + str(lat))
        response = response.json()
        score = response["score"]
        numero_rue = response["name"]
        code_postale = response["postcode"]
        adresse_API = numero_rue + code_postale
        fiche_a_traiter.adresse_finale = adresse_API
        return(score, fiche_a_traiter)

    def geocodage_par_lot(self, fiches_a_traiter : List[FicheAdresse]) -> Tuple[List[float], List[FicheAdresse]]:
        n = len(fiches_a_traiter)
        scores = []
        for i in range (n):
            score, fiche = BANClient.geocodage_par_fiche(self, fiches_a_traiter[i])
            fiches_a_traiter[i]=fiche
            scores.append(score)
        return(scores, fiches_a_traiter)

    def reverse_par_lot(self, fiches_a_traiter : List[FicheAdresse]) -> Tuple[List[float], List[FicheAdresse]]:
        n = len(fiches_a_traiter)
        scores = []
        for i in range (n):
            score, fiche = BANClient.reverse_par_fiche(self, fiches_a_traiter[i])
            fiches_a_traiter[i]=fiche
            scores.append(score)
        return(scores, fiches_a_traiter)
