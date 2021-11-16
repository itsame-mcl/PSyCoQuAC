from PyInquirer import prompt
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.menu import MenuPrincipalView
from ViewLayer.CLI.menu import Session
from BusinessLayer.LocalServices.Gestion.agent_service import AgentService


class ChangerDroitsView(AbstractView):
    def __init__(self, session : Session) -> None:
        self.__questions = [{'type': 'input','name': 'id_agent','message': "De quel agent voulez-vous changer les droits ?"}]
        self.__questions2 = [{'type': 'list','name': 'choix','message': "Souhaitez-vous changer les droits d'un autre agent ?",
                            'choices': ['O) Oui', 'N) Non']}]

    def make_choice(self):
        answers = prompt(self.__questions)
        probleme = AgentService.changer_droits(answers['id_agent'])
        if not(probleme):
            print("L'enregistrement a échoué. Veuillez réessayer ultérieurement.")
        answers2 = prompt(self.__questions2)
        if 'o' in str.lower(answers2['choix']):
            return ChangerDroitsView(self.__session)
        else :
            return MenuPrincipalView()
        