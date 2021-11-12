from DataLayer.DAO import dao_fiche_adresse
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.menu import MenuPrincipalView
from ViewLayer.CLI.session import Session
from  BusinessLayer.LocalServices.TraitementFA.controle_reprise_service import ControleRepriseService
from PyInquirer import prompt

class ControlerView(AbstractView):

    def __init__(self, session : Session, curseur : int = 0) -> None:
        self.__questions = [{'type': 'list','name': 'choix','message': 'Que voulez-vous faire ?',
                            'choices': ['c) Les données sont correctes','i) Les données sont incorrectes ', 
                            'p) Retourner à la fiche précédente', 's) Passer à la fiche suivante', 'm) Retourner au menu principal']}]
        self.__questions2 = [{'type':'list', 'name':'choix', 'message': 'Confirmez-vous votre décision ?', 'choices': ['Oui', 'Non']}]
    
    def display_info(self, session : Session, curseur : int):
        pot = dao_fiche_adresse.recupere_pot(session.agent_id) 
        fiche = pot[curseur]
        print('Fiche adresse n°' + str(fiche.fiche_id) + '\n   Données initiales :\nAdresse initiale : ' + str(fiche.adresse_initiale) + '\n   Données API :\nAdresse finale : '  + str(fiche.adresse_finale) + '\nCoordonnées GPS : ' + str(fiche.coords_wgs84))

    def make_choice(self, session : Session, curseur : int): # curseur = l'emplacement de la fiche en contrôle dans la liste
        pot = dao_fiche_adresse.recupere_pot(session.agent_id) 
        fiche = pot[curseur]
        answers = prompt(self.__questions)
        if 'c' in str.lower(answers['choix']) :
            answers2 = prompt(self.__questions2)
            if str.lower(answers2['choix']) == 'oui' :
                probleme = ControleRepriseService.modifier_fiche(fiche.fiche_id, {'code_res' : 'VC'})
                if not(probleme):
                    print("Le contrôle a échoué. Veuillez réessayer ultérieurement.")
                    return ControlerView(session, curseur+1)
                else:
                    return ControlerView(session, curseur+1)
            elif str.lower(answers2['choix']) == 'non':
                return ControlerView(session, curseur)
        elif 'i'in str.lower(answers['choix']) :
            answers2 = prompt(self.__questions2)
            if str.lower(answers2['choix']) == 'oui' :
                probleme = ControleRepriseService.modifier_fiche(fiche.fiche_id, {'code_res' : 'TR'})
                if not(probleme):
                    print("Le contrôle a échoué. Veuillez réessayer ultérieurement.")
                    return ControlerView(session, curseur+1)
                else:
                    return ControlerView(session, curseur+1)
            elif str.lower(answers2['choix']) == 'non':
                return ControlerView(session, curseur)
        elif 'p' in str.lower(answers['choix']) :
            curseur = (curseur-1) % len(pot)
            return ControlerView(session, curseur)
        elif 's'in str.lower(answers['choix']) :
            curseur = (curseur+1) % len(pot)
            return ControlerView(session, curseur)
        elif 'm' in str.lower(answers['choix']) :
            return MenuPrincipalView(session)