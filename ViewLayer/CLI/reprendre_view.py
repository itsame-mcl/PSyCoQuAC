from DataLayer import DAO
from DataLayer.DAO import dao_fiche_adresse
from ViewLayer.CLI.menu import MenuPrincipalView
from ViewLayer.CLI.session import Session

from PyInquirer import prompt

from ViewLayer.CLI.session import Session

class ReprendreFiche:

    def __init__(self) -> None:

        self.__questions = [{'type': 'list','name': 'choix','message': 'Que voulez-vous faire ?',
                            'choices': ["a) Modifier l'adresse",'c) Modifier les coordonnées GPS', 'v) Valider la fiche', 'd) Marquer la fiche en déchet',  'p) Passer à la fiche précédente', 's) Passer à la fiche suivante', 'm) Retourner au menu principal']}]
        self.__questions2 = [{'type':'list', 'name':'choix', 'message': 'Confirmez-vous ?', 'choices':['Oui', 'Non']}]
        self.__questions3 = [{'type': 'input','name': 'numero','message': 'Numéro de voie :'}, {'type': 'input','voie': 'nom','message': 'Nom de la voie',},
            {'type': 'input','name': 'cd','message': 'Code postal :'}, {'type': 'input','name': 'ville','message': 'Ville :'}]
        self.__questions4 = [{'type': 'list', 'name' : 'choix', 'message': "Voulez vous resoumettre la fiche à l'API ?", 'choices':['Oui', 'Non']}]
        self.__questions5 = [{'type': 'input','name': 'lat','message': 'Latitude :'}, {'type': 'input','name': 'lon','message': 'Longitude :'}]
    
    def reprendre_fiche(self, curseur = 0): # curseur = l'emplacement de la fiche en contrôle dans la liste
        pot = dao_fiche_adresse.recupere_pot(Session.agent_id) 
        fiche = pot[curseur] # On récupère la fiche dans le pot de l'agent
        print('Fiche adresse n°:' + str(fiche.fiche_id) + 'Données initiales : adresse initiale : ' + str(fiche.adresse_initiale) + 'Données API : Adresse finale : '  + str(fiche.adresse_finale) + 'Coordonnées GPS :' + str(fiche.coords_wgs84))
        answers = prompt(self.__questions)
        if 'a)' in str.lower(answers['choix']) :
            answers3 = prompt(self.__questions3)
            nouvelle_adresse = Adresse('numero', 'voie', 'cd', 'ville')
            res = dao_fiche_adresse.from(fiche, { 'adresse_finale': nouvelle_adresse})
            answers4 = prompt(self.__questions4)
            if str.lower(answer4['choix']) == 'Oui' :
                # Resoumettre à l'API
            elif str.lower(answer4['choix']) == 'Non' :
                return ReprendreFiche.reprendre_fiche()
        elif 'c)' in str.lower(answers['choix']) :
            answers5 = prompt(self.__questions5)
            nouvelles_coords = ('lat', 'lon')
            res = dao_fiche_adresse.from(fiche, {'coords_wgs84': nouvelles_coords})
            answers4 = prompt(self.__questions4)
                        if str.lower(answer4['choix']) == 'Oui' :
                # Resoumettre à l'API
            elif str.lower(answer4['choix']) == 'Non' :
                return ReprendreFiche.reprendre_fiche()
        elif 'v)' in str.lower(answers['choix']) :
            answers2 = prompt(self.__questions2)
            if str.lower(answers2['choix']) == 'Oui' :
                res = dao_fiche_adresse.modifier_fiche_adresse(fiche, {'code_res' : 'VR'})
                return ReprendreFiche.reprendre_fiche()
            elif str.lower(answer2['choix']) == 'Non':
                return ReprendreFiche.reprendre_fiche()
        elif 'd)'in str.lower(answers['choix']) :
            answers2 = prompt(self.__questions2)
            if str.lower(answers2['choix']) == 'Oui' :
                res = dao_fiche_adresse.modifier_fiche_adresse(fiche, {'code_res' : 'DR'})
                return ReprendreFiche.reprendre_fiche()
            elif str.lower(answer2['choix']) == 'Non':
                return ReprendreFiche.reprendre_fiche()
        elif 'p)' in str.lower(answers['choix']) :
            curseur = (curseur-1) % len(pot)
            return ReprendreFiche.reprendre_fiche()
        elif 's)'in str.lower(answers['choix']) :
            curseur = (curseur+1) % len(pot)
            return ReprendreFiche.reprendre_fiche()
        elif 'm)' in str.lower(answers['choix']) :
            from ViewLayer.CLI.menu import MenuPrincipalView
            return MenuPrincipalView()