from DataLayer import DAO
from DataLayer.DAO import dao_fiche_adresse
from ViewLayer.CLI.menu import MenuPrincipalView
from ViewLayer.CLI.session import Session

from PyInquirer import prompt

from ViewLayer.CLI.session import Session

class ControlerFiche:

    def __init__(self) -> None:

        self.__questions = [{'type': 'list','name': 'choix','message': 'Que voulez-vous faire ?',
                            'choices': ['c) Valider les données, elles sont correctes','i) Invalider les données, elles sont incorrectes ', 'p) Passer à la fiche précédente', 's) Passer à la fiche suivante', 'm) Retourner au menu principal']}]
        self.__questions2 = [{'type':'list', 'name':'choix', 'message': 'Confirmez-vous ?', 'choices':['Oui', 'Non']}]
    
    def controle_fiche(self, curseur = 0): # curseur = l'emplacement de la fiche en contrôle dans la liste
        pot = dao_fiche_adresse.recupere_pot(Session.agent_id) 
        fiche = pot[curseur] # On récupère la fiche dans le pot de l'agent
        print('Fiche adresse n°:' + str(fiche.fiche_id) + 'Données initiales : adresse initiale : ' + str(fiche.adresse_initiale) + 'Données API : Adresse finale : '  + str(fiche.adresse_finale) + 'Coordonnées GPS :' + str(fiche.coords_wgs84))
        answers = prompt(self.__questions)
        if 'c)' in str.lower(answers['choix']) :
            answers2 = prompt(self.__questions2)
            if str.lower(answers2['choix']) == 'Oui' :
                res = dao_fiche_adresse.modifier_fiche_adresse(fiche, {'code_res' : 'VC'})
                return ControlerFiche.controle_fiche()
            elif str.lower(answer2['choix']) == 'Non':
                return ControlerFiche.controle_fiche()
        elif 'i)'in str.lower(answers['choix']) :
            answers2 = prompt(self.__questions2)
            if str.lower(answers2['choix']) == 'Oui' :
                res = dao_fiche_adresse.modifier_fiche_adresse(fiche, {'code_res' : 'TR'})
                return ControlerFiche.controle_fiche()
            elif str.lower(answer2['choix']) == 'Non':
                return ControlerFiche.controle_fiche()
        elif 'p)' in str.lower(answers['choix']) :
            curseur = (curseur-1) % len(pot)
            return ControlerFiche.controle_fiche()
        elif 's)'in str.lower(answers['choix']) :
            curseur = (curseur+1) % len(pot)
            return ControlerFiche.controle_fiche()
        elif 'm)' in str.lower(answers['choix']) :
            from ViewLayer.CLI.menu import MenuPrincipalView
            return MenuPrincipalView()