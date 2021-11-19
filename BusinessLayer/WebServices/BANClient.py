from typing import Tuple
from time import time_ns, sleep
import requests
import csv
import os

from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
from BusinessLayer.BusinessObjects.adresse import Adresse
from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from utils.singleton import Singleton


class BANClient(metaclass=Singleton):
    def __init__(self):
        self.__wait_ns = 2000000
        self.__lastcall = 0

    @staticmethod
    def __json_to_fa(json_data, fiche):
        coordonnees_gps = json_data["geometry"]["coordinates"]
        fiche.coords_wgs84 = tuple(coordonnees_gps)
        adresse_api = Adresse(json_data["properties"]["housenumber"], json_data["properties"]["street"],
                              json_data["properties"]["postcode"], json_data["properties"]["city"])
        fiche.adresse_finale = adresse_api
        return fiche

    def geocodage_par_fiche(self, fiche_a_traiter: FicheAdresse) -> Tuple[float, FicheAdresse]:
        adresse = str(fiche_a_traiter.adresse_finale).replace(" ", "+")
        if time_ns() - self.__lastcall < self.__wait_ns:
            sleep((time_ns() - self.__lastcall) / 1000000000)
        response = requests.get("https://api-adresse.data.gouv.fr/search/?q=" + adresse + "&limit=1&autocomplete=0")
        self.__lastcall = time_ns()
        response = response.json()
        score = response["features"][0]["properties"]["score"]
        fiche_a_traiter = self.__json_to_fa(response["features"][0], fiche_a_traiter)
        return score, fiche_a_traiter

    def reverse_par_fiche(self, fiche_a_traiter: FicheAdresse) -> Tuple[float, FicheAdresse]:
        if len(fiche_a_traiter.coords_wgs84) == 0:
            raise ValueError('La fiche adresse ne possède pas de coordonnées GPS')
        coordonnees_gps = fiche_a_traiter.coords_wgs84
        lon = coordonnees_gps[0]
        lat = coordonnees_gps[1]
        if time_ns() - self.__lastcall < self.__wait_ns:
            sleep((time_ns() - self.__lastcall) / 1000000000)
        response = requests.get("https://api-adresse.data.gouv.fr/reverse/?lon=" + str(lon) + "&lat=" + str(lat))
        self.__lastcall = time_ns()
        response = response.json()
        score = response["features"][0]["properties"]["score"]
        fiche_a_traiter = self.__json_to_fa(response["features"][0], fiche_a_traiter)
        return score, fiche_a_traiter

    @staticmethod
    def geocodage_par_lot(id_lot: int,  seuil_score: float = 0.9) -> bool:
        lot = DAOFicheAdresse().recuperer_lot(id_lot)
        fiches_a_traiter = list()
        for fiche in lot:
            if fiche.code_res == "TA":
                fiches_a_traiter.append(fiche)
        try:
            with open("search.csv", "w") as file:
                writer = csv.writer(file)
                writer.writerow(["id", "adresse", "postcode", "city"])
                for fiche in fiches_a_traiter:
                    writer.writerow(
                        [str(fiche.fiche_id), str(fiche.adresse_finale.numero) + " " + str(fiche.adresse_finale.voie),
                         str(fiche.adresse_finale.cp), str(fiche.adresse_finale.ville)])
            with open("search.csv", "r") as file:
                response = requests.post(url="https://api-adresse.data.gouv.fr/search/csv/", data={
                    'columns': ["adresse", "city"], 'postcode': "postcode", 'result_columns': [
                        "result_housenumber", "result_name", "result_postcode", "result_city", "latitude", "longitude",
                        "result_score"]}, files={'data': file})
            with open("answer.csv", "wb") as reponse:
                reponse.write(response.content)
            with open("answer.csv", "r") as reponse:
                reader = csv.DictReader(reponse, delimiter=",")
                for index, data in zip(range(len(fiches_a_traiter)), reader):
                    if data["result_housenumber"] == "" and data["result_name"] == "" and data[
                      "result_postcode"] == "" and data["result_city"] == "":
                        pass
                    else:
                        adresse_api = Adresse(data["result_housenumber"], data["result_name"], data["result_postcode"],
                                              data["result_city"])
                        fiches_a_traiter[index].adresse_finale = adresse_api
                    if data["longitude"] == "" or data["latitude"] == "":
                        fiches_a_traiter[index].coords_wgs84 = tuple()
                    else:
                        fiches_a_traiter[index].coords_wgs84 = (data["longitude"], data["latitude"])
                    if data["result_score"] == "" or float(data["result_score"]) < seuil_score:
                        fiches_a_traiter[index].code_res = "TR"
                    else:
                        fiches_a_traiter[index].code_res = "TH"
                    DAOFicheAdresse().modifier_fiche_adresse(fiches_a_traiter[index])
            res = True
        except Exception:
            res = False
        finally:
            if os.path.exists("search.csv"):
                os.remove("search.csv")
            if os.path.exists("answer.csv"):
                os.remove("answer.csv")
        return res
