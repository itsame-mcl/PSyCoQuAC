from typing import Tuple, List
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

    @staticmethod
    def __json_to_fa(json_data, fiche):
        """

        :param json_data:
        :param fiche:
        :return:
        """
        coordonnees_gps = json_data["geometry"]["coordinates"]
        fiche.coords_wgs84 = tuple(coordonnees_gps)
        adresse_api = Adresse(json_data["properties"].setdefault("housenumber", ""),
                              json_data["properties"].setdefault("street", ""),
                              json_data["properties"].setdefault("postcode", ""),
                              json_data["properties"].setdefault("city", ""))
        fiche.adresse_finale = adresse_api
        return fiche

    def geocodage_par_fiche(self, fiche_a_traiter: FicheAdresse) -> Tuple[float, FicheAdresse]:
        """

        :param fiche_a_traiter:
        :return:
        """
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
        """

        :param fiche_a_traiter:
        :return:
        """
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
    def geocodage_par_lot(fiches_a_traiter: List[FicheAdresse], seuil_score: float = 0.8,
                          verbose=False) -> List[FicheAdresse]:
        """

        :param fiches_a_traiter:
        :param seuil_score:
        :param verbose:
        :return:
        """
        try:
            if verbose:
                print("Préparation de la requête API...")
            query_string = io.StringIO()
            writer = csv.writer(query_string)
            writer.writerow(["id", "adresse", "postcode", "city"])
            for fiche in fiches_a_traiter:
                writer.writerow(
                    [str(fiche.fiche_id), str(fiche.adresse_finale.numero) + " " + str(fiche.adresse_finale.voie),
                     str(fiche.adresse_finale.cp), str(fiche.adresse_finale.ville)])
            query_string.seek(0)
            query_binary = io.BytesIO()
            query_binary.encoding = "utf-8"
            query_binary.write(query_string.read().encode('utf-8'))
            query_string.close()
            query_binary.seek(0)
            if verbose:
                print("Envoi de la requête à l'API...")
            response = requests.post(url="https://api-adresse.data.gouv.fr/search/csv/", data={
                'columns': ["adresse", "city"], 'postcode': "postcode", 'result_columns': [
                    "result_housenumber", "result_name", "result_postcode", "result_city", "latitude", "longitude",
                    "result_score"]}, files={'data': query_binary.read()})
            if verbose:
                print("Réponse de l'API reçue, analyse des résultats...")
            query_binary.close()
            answer_binary = io.BytesIO()
            answer_binary.encoding = "utf-8"
            answer_binary.write(response.content)
            answer_binary.seek(0)
            answer_string = io.StringIO()
            answer_string.write(answer_binary.read().decode())
            answer_binary.close()
            answer_string.seek(0)
            reader = csv.DictReader(answer_string, delimiter=",")
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
            answer_string.close()
            if verbose:
                print("Analyse des résultats terminée !")
        except Exception:
            if verbose:
                print("Des erreurs sont survenues dans le traitement de la requête API.")
            fiches_a_traiter = None
        return fiches_a_traiter
