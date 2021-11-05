from PyInquirer import prompt
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.menu import MenuPrincipalView
from ViewLayer.CLI.session import Session
from BusinessLayer.LocalServices.Gestion.agent_service import AgentService

class ChangerDroitsView(AbstractView):

    def __init__(self, session) -> None:
        self.__questions = [{'type': 'input','name': 'id_agent','message': "De quel agent voulez-vous changer les droits ?"}]

    def make_choice(self, session : Session):
        answers = prompt(self.__questions)
        probleme = AgentService.changer_droits(answers['id_agent'])
        if not(probleme):
            print("L'enregistrement a échoué. Veuillez réessayer ultérieurement.")
        return MenuPrincipalView(session)
        