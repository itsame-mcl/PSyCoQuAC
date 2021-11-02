from random import *

class AffectationService():
    def echantilloner_fiches(echantillon, taille_echantillon):
        n = len(echantillon)
        l = [i for i in range (n)]
        liste_aleatoire = sample(l, taille_echantillon) #Contruction d'une liste aléatoire d'entier compris entre 0 et n-1 de taille taille_echantillon 
        liste_echantillonne = []
        for i in range (taille_echantillon) :
            liste_echantillonne.append(echantillon[liste_aleatoire[i]])
        return liste_echantillonne

    def appliquer_repartition(session_utilisateur, repartition):