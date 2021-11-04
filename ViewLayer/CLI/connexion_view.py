from pprint import pprint
from PyInquirer import  prompt
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.session import Session

class Connexion(AbstractView):
    
    def __init__(self) -> None:
        self.__questions = [
            {
                'type': 'input',
                'name': 'first_name',
                'message': 'What\'s your first name',
            },
            {
                'type': 'input',
                'name': 'last_name',
                'message': 'What\'s your last name',
            },
            {
                'type': 'input',
                'name': 'pseudo',
                'message': 'What\'s your pseudo',
            },
            {
                'type': 'password',
                'name': 'password',
                'message': 'What\'s your password. Your password should be '\
                    'at least 10 characters, with at least one capital letter ' \
                    'one number and one special character',
                'validate': PasswordValidator
            }
        ]

    def display_info(self):
        print(f"Bonjour {Session().prenom}, please choose some pokemon")

    def make_choice(self):
        answers = prompt(self.__questions)
        pprint(answers)
        from view.start_view import StartView
        return StartView()
