from PyInquirer import prompt
from BusinessLayer.LocalServices.Gestion.session_service import SessionService
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.menu import MenuPrincipalView
from ViewLayer.CLI.session import Session
from BusinessLayer.BusinessObjects.agent import Agent
import ViewLayer.CLI.start_view as start


class ConnexionView(AbstractView):
    def __init__(self) -> None:
        self.__questions = [{'type': 'input', 'name': 'nom_utilisateur', 'message': "Nom d'utilisateur"},
                            {'type': 'password', 'name': 'mot_de_passe', 'message': 'Mot de passe :'}]
        self.__prompt_reessayer = [{'type': 'confirm', 'name': 'retry', 'message': "Nom d'utilisateur ou "
                "mot de passe incorrect. Voulez-vcus réessayer ?", 'default': True}]

    def make_choice(self):
        answers = prompt(self.__questions)
        agent = SessionService().ouvrir_session(answers['nom_utilisateur'],answers['mot_de_passe'])
        if not (isinstance(agent, Agent)):
            #Ah ah ah... Vous n'avez pas dis le mot magique !
            reessayer = prompt(self.__prompt_reessayer)
            if reessayer['retry']:
                return ConnexionView()
            else:
                return start.StartView()
        else:
            Session().agent = agent
            return MenuPrincipalView()
