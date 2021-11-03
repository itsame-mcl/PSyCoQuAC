from random import *
from DataLayer import DAO as dao

class AffectationService():

    def echantilloner_fiches(echantillon, nb_fiche_à_controler):
        n = len(echantillon)
        l = [i for i in range (n)]
        liste_aleatoire = sample(l, nb_fiche_à_controler) #Contruction d'une liste aléatoire d'entier compris entre 0 et n-1 de taille nb_fiche_à_controler 
        liste_echantillonne = []
        for i in range (nb_fiche_à_controler) :
            liste_echantillonne.append(echantillon[liste_aleatoire[i]])
        return liste_echantillonne

    def appliquer_repartition(session_utilisateur, repartition): # repartition est un dictionnaire, avec comme clés les agents_id et comme valeurs les fiches_id 
        agents_id = repartition.keys()
        for id in agents_id:
            dao.DAOFicheAdresse.affecter_fiches_adresse(id, repartition[str(id)])