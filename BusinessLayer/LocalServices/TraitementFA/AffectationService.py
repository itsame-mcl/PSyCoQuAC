from random import *

class AffectationService():
    def echantilloner_fiches(echantillon, taille_echantillon):
        n = len(echantillon)
        liste_aleatoire = []
        while len(liste_aleatoire) != taille_echantillon :
            a = randint(0, n-1)
            if a in not liste_aleatoire :
                liste_aleatoire.append(a)
        liste_echantillonne = []
        for i in range (taille_echantillon) :
            liste_echantillonne.append(echantillon[liste_aleatoire[i]])
        return liste_echantillonne

    def appliquer_repartition(session_utilisateur, repartition):