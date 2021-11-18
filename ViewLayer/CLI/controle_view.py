from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.menu import MenuPrincipalView
from ViewLayer.CLI.session import Session
from BusinessLayer.LocalServices.TraitementFA.controle_reprise_service import ControleRepriseService
from PyInquirer import prompt


class ControlerView(AbstractView):
    def __init__(self, curseur: int = 0) -> None:
        self.__curseur = curseur
        self.__questions = [{'type': 'list', 'name': 'choix', 'message': 'Que voulez-vous faire ?',
                             'choices': ['c) Les données sont correctes', 'i) Les données sont incorrectes ',
                                         'p) Retourner à la fiche précédente', 's) Passer à la fiche suivante',
                                         'm) Retourner au menu principal']}]
        self.__questions2 = [
            {'type': 'list', 'name': 'choix', 'message': 'Confirmez-vous votre décision ?', 'choices': ['Oui', 'Non']}]

    def display_info(self):
        pot = ControleRepriseService().consulter_pot(Session().agent.agent_id)
        fiche = pot[self.__curseur]
        print('Fiche adresse n°' + str(fiche.fiche_id) + '\n   Données initiales :\nAdresse initiale : ' + str(
            fiche.adresse_initiale) + '\n   Données API :\nAdresse finale : ' + str(
            fiche.adresse_finale) + '\nCoordonnées GPS : ' + str(fiche.coords_wgs84))

    def make_choice(self):
        pot = ControleRepriseService().consulter_pot(Session().agent.agent_id)
        fiche = pot[self.__curseur]
        answers = prompt(self.__questions)
        if 'c' in str.lower(answers['choix']):
            answers2 = prompt(self.__questions2)
            if str.lower(answers2['choix']) == 'oui':
                fiche.code_res = "VC"
                succes = ControleRepriseService().modifier_fiche(fiche)
                if not succes:
                    print("Le contrôle a échoué. Veuillez réessayer ultérieurement.")
                    return ControlerView(self.__curseur + 1)
                else:
                    return ControlerView(self.__curseur + 1)
            elif str.lower(answers2['choix']) == 'non':
                return ControlerView(self.__curseur)
        elif 'i' in str.lower(answers['choix']):
            answers2 = prompt(self.__questions2)
            if str.lower(answers2['choix']) == 'oui':
                fiche.code_res = "TR"
                succes = ControleRepriseService().modifier_fiche(fiche)
                if not succes:
                    print("Le contrôle a échoué. Veuillez réessayer ultérieurement.")
                    return ControlerView(self.__curseur + 1)
                else:
                    return ControlerView(self.__curseur + 1)
            elif str.lower(answers2['choix']) == 'non':
                return ControlerView(self.__curseur)
        elif 'p' in str.lower(answers['choix']):
            curseur = (self.__curseur - 1) % len(pot)
            return ControlerView(curseur)
        elif 's' in str.lower(answers['choix']):
            curseur = (self.__curseur + 1) % len(pot)
            return ControlerView(curseur)
        elif 'm' in str.lower(answers['choix']):
            return MenuPrincipalView()
