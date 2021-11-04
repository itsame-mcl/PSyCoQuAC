from PyInquirer import prompt
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.session import Session
import ViewLayer

class MenuPrincipalView(AbstractView):

    def __init__(self):
        self.__questions = [{'type': 'list','name': 'choix','message': 'Bonjour '+str(Session().prenom),
                            'choices': ['Consulter son pot','Se déconnecter']}]

    def affichage(self):
        with open('outils graphiques/bannière.txt', 'r', encoding = "utf-8") as asset:
            print(asset.read())

    def make_choice(self):
        answers = prompt(self.__questions)
        if 'pot' in str.lower(answers['choix']) :
            from ViewLayer.ConsulterPotView import CheckBoxExampleView
            return CheckBoxExampleView()
        elif str.lower(answers['choix']) == 'se déconnecter' or str.lower(answers['choix']) == 'se deconnecter' :
            return ViewLayer.DeconnexionView.deconnexion()