from typing import List, Tuple
import requests

from time import time_ns, sleep
from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from utils.singleton import Singleton


class BANClient(metaclass=Singleton):
    def __init__(self):
        self.__wait_ns = 2000000
        self.__lastcall = 0

    def geocodage_par_fiche(self, fiche_a_traiter: FicheAdresse) -> Tuple[float, FicheAdresse]:
        adresse = fiche_a_traiter.adresse_initiale
        adresse = adresse.replace(" ", "+")
        if time_ns() - self.__lastcall < self.__wait_ns:
            sleep((time_ns() - self.__lastcall)/1000000000)
        response = requests.get("https://api-adresse.data.gouv.fr/search/?q=" + str(adresse))
        self.__lastcall = time_ns()
        response = response.json()
        score = response["score"]
        coordonnees_gps = response["coordinates"]
        fiche_a_traiter.coords_WGS84 = coordonnees_gps
        numero_rue = response["name"]
        code_postale = response["postcode"]
        adresse_api = numero_rue + code_postale
        fiche_a_traiter.adresse_finale = adresse_api
        return score, fiche_a_traiter

    def reverse_par_fiche(self, fiche_a_traiter: FicheAdresse) -> Tuple[float, FicheAdresse]:
        if len(fiche_a_traiter.coords_wgs84) == 0:
            raise ValueError('La FicheAdresse ne possède pas de coordonnées GPS')
        coordonnees_gps = fiche_a_traiter.coords_wgs84
        lon = coordonnees_gps[0]
        lat = coordonnees_gps[1]
        if time_ns() - self.__lastcall < self.__wait_ns:
            sleep((time_ns() - self.__lastcall)/1000000000)
        response = requests.get("https://api-adresse.data.gouv.fr/reverse/?lon=" + str(lon) + "&lat=" + str(lat))
        self.__lastcall = time_ns()
        response = response.json()
        score = response["score"]
        numero_rue = response["name"]
        code_postale = response["postcode"]
        adresse_api = numero_rue + code_postale
        fiche_a_traiter.adresse_finale = adresse_api
        return score, fiche_a_traiter

    def geocodage_par_lot(self, fiches_a_traiter: List[FicheAdresse]) -> Tuple[List[float], List[FicheAdresse]]:
        n = len(fiches_a_traiter)
        scores = []
        for i in range(n):
            score, fiche = self.geocodage_par_fiche(fiches_a_traiter[i])
            fiches_a_traiter[i] = fiche
            scores.append(score)
        return scores, fiches_a_traiter

    def reverse_par_lot(self, fiches_a_traiter: List[FicheAdresse]) -> Tuple[List[float], List[FicheAdresse]]:
        n = len(fiches_a_traiter)
        scores = []
        for i in range(n):
            score, fiche = self.reverse_par_fiche(fiches_a_traiter[i])
            fiches_a_traiter[i] = fiche
            scores.append(score)
        return scores, fiches_a_traiter
