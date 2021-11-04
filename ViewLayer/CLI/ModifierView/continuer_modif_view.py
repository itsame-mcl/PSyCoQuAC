from PyInquirer import prompt
from ViewLayer.CLI.menu import MenuPrincipalView
from ViewLayer.CLI.ModifierView.modifier_compte_view import ModifierCompteView
from ViewLayer.CLI.session import Session

class ContinuerModifView:

    def __init__(self, session : Session) -> None:
        self.__questions2 = [{'type': 'list','name': 'choix','message': 'Souhaitez-vous modifier autre chose ?',
                            'choices': ['1) Oui', '2) Non']}]
    
    def continuer(self, session : Session):
        answers2 = prompt(self.__questions2)
        if '1' in answers2['choix']:
            return ModifierCompteView(session)
        else:
            return MenuPrincipalView(session)