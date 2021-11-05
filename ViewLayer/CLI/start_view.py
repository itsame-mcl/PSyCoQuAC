from ViewLayer.CLI.abstract_view import AbstractView
from PyInquirer import prompt
from ViewLayer.CLI.connexion_view import ConnexionView

class StartView(AbstractView):

    def __init__(self):
        self.__questions = [{'type': 'list','name': 'choix','message': 'Que voulez-vous faire ?',
                            'choices': ['C) Se connecter', "Q) Quitter l'application"]}]

    def display_info(self):
        with open('outils graphiques/bannière.txt', 'r', encoding = "utf-8") as asset:
            print(asset.read())

    def make_choice(self):
        answers = prompt(self.__questions)
        if 'q' in str.lower(answers['choix']):
            return None
        else:
            return ConnexionView()