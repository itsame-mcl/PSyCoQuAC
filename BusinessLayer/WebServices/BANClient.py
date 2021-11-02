import requests

class BANClient :
    def __init__(self) :

    
    def geocodage_par_fiche(self, fiche_a_traiter):
        adresse = fiche_a_traiter.adresse_initiale
        adresse = adresse.replace(" ", "+")
        response = requests.get("https://api-adresse.data.gouv.fr/search/?q=" + adresse)
        response = response.json()
        score = response["score"]
        coordonnees_gps = response["coordinates"]
        fiche_a_traiter.coords_WGS84 = coordonnees_gps
        numero_rue = response["name"]
        code_postale = response["postcode"]
        adresse_API = numero_rue + code_postale
        fiche_a_traiter.adresse_finale = adresse_API
        return(score, fiche_a_traiter)
    
    def reverse_par_fiche(self, fiche_a_traiter):
        if len(fiche_a_traiter.coords_WGS84) == 0 :
            raise ValueError('La FicheAdresse ne possède pas de coordonnées GPS')
        coordonnees_gps = fiche_a_traiter.coords_WGS84
        lon=coordonnees_gps[0]
        lat=coordonnees_gps[1]
        response = requests.get("https://api-adresse.data.gouv.fr/reverse/?lon=" + lon + "&lat=" + lat)
        response = response.json()
        score = response["score"]
        numero_rue = response["name"]
        code_postale = response["postcode"]
        adresse_API = numero_rue + code_postale
        fiche_a_traiter.adresse_finale = adresse_API
        return(score, fiche_a_traiter)

    def geocodage_par_lot(self, fiches_a_traiter):
        n = len(fiches_a_traiter)
        scores = []
        for i in range (n):
            score, fiche = geocodage_par_fiche(self, fiches_a_traiter[i])
            fiches_a_traiter[i]=fiche
            scores.append(score)
        return(scores, fiches_a_traiter)

    def reverse_par_lot(self, fiches_a_traiter):
        n = len(fiches_a_traiter)
        scores = []
        for i in range (n):
            score, fiche = reverse_par_fiche(self, fiches_a_traiter[i])
            fiches_a_traiter[i]=fiche
            scores.append(score)
        return(scores, fiches_a_traiter)


    
