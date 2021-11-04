from PyInquirer import prompt
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.session import Session

class MenuView(AbstractView):

    def __init__(self):
        self.__questions = [
            {
                'type': 'list',
                'name': 'choix',
                'message': 'Bonjour '+str(Session().user_name),
                'choices': [
                    'Next'
                    , 'Checkbox example'
                    , 'Sign In example'

                ]
            }
        ]

    def display_info(self):
        with open('utils/banner.png', 'r') as asset:
            print(asset.read())

#    def make_choice(self):
#        reponse = prompt(self.__questions)
#        if reponse['choix'] == 'Next':
#            pass
#        elif reponse['choix'] == 'Checkbox example':
#            from view.checkbox_example_view import CheckBoxExampleView
#            return CheckBoxExampleView()
#        elif reponse['choix'] == 'Sign In example':
#            from view.sign_in_example import SignInExample
#            return SignInExample()

