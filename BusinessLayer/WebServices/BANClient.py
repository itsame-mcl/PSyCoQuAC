from typing import List, Tuple
from time import time_ns, sleep
import requests
import csv
import io

from BusinessLayer.BusinessObjects.adresse import Adresse
from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from utils.singleton import Singleton


class BANClient(metaclass=Singleton):
    def __init__(self):
        self.__wait_ns = 2000000
        self.__lastcall = 0

    def __json_to_fa(self, json_data, fiche):
        coordonnees_gps = json_data["coordinates"]
        fiche.coords_wgs84 = coordonnees_gps
        adresse_api = Adresse(json_data["housenumber"], json_data["street"], json_data["postcode"], json_data["city"])
        fiche.adresse_finale = adresse_api
        return fiche

    def geocodage_par_fiche(self, fiche_a_traiter: FicheAdresse) -> Tuple[float, FicheAdresse]:
        adresse = str(fiche_a_traiter.adresse_finale).replace(" ", "+")
        if time_ns() - self.__lastcall < self.__wait_ns:
            sleep((time_ns() - self.__lastcall)/1000000000)
        response = requests.get("https://api-adresse.data.gouv.fr/search/?q=" + adresse)
        self.__lastcall = time_ns()
        response = response.json()
        score = response["score"]
        fiche_a_traiter = self.__json_to_fa(response, fiche_a_traiter)
        return score, fiche_a_traiter

    def reverse_par_fiche(self, fiche_a_traiter: FicheAdresse) -> Tuple[float, FicheAdresse]:
        if len(fiche_a_traiter.coords_wgs84) == 0:
            raise ValueError('La fiche adresse ne possède pas de coordonnées GPS')
        coordonnees_gps = fiche_a_traiter.coords_wgs84
        lon = coordonnees_gps[0]
        lat = coordonnees_gps[1]
        if time_ns() - self.__lastcall < self.__wait_ns:
            sleep((time_ns() - self.__lastcall)/1000000000)
        response = requests.get("https://api-adresse.data.gouv.fr/reverse/?lon=" + str(lon) + "&lat=" + str(lat))
        self.__lastcall = time_ns()
        response = response.json()
        score = response["score"]
        fiche_a_traiter = self.__json_to_fa(response, fiche_a_traiter)
        return score, fiche_a_traiter

    def geocodage_par_lot(self, fiches_a_traiter: List[FicheAdresse]) -> Tuple[List[float], List[FicheAdresse]]:
        stream = io.StringIO()
        writer = csv.writer(stream)
        writer.writerow(["id","adresse","postcode","city"])
        for fiche in fiches_a_traiter:
            writer.writerow([str(fiche.fiche_id), str(fiche.adresse_finale.numero) + " " + str(fiche.adresse_finale.voie),
                             str(fiche.adresse_finale.cp), str(fiche.adresse_finale.ville)])
        stream.seek(0)
        file = io.BytesIO()
        file.write(stream.getvalue().encode())
        file.seek(0)
        file.name = f'search.csv'
        response = requests.post(url="https://api-adresse.data.gouv.fr/search/csv/", data=file)
        return response

    def reverse_par_lot(self, fiches_a_traiter: List[FicheAdresse]) -> Tuple[List[float], List[FicheAdresse]]:
        n = len(fiches_a_traiter)
        scores = []
        for i in range(n):
            score, fiche = self.reverse_par_fiche(fiches_a_traiter[i])
            fiches_a_traiter[i] = fiche
            scores.append(score)
        return scores, fiches_a_traiter
