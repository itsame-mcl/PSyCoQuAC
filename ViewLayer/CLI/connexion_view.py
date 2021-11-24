from PyInquirer import prompt
from BusinessLayer.LocalServices.Gestion.session_service import SessionService
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.menu import MenuPrincipalView
from ViewLayer.CLI.session import Session
from BusinessLayer.BusinessObjects.agent import Agent


class ConnexionView(AbstractView):
    def __init__(self) -> None:
        self.__questions = [{'type': 'input', 'name': 'nom_utilisateur', 'message': "Nom d'utilisateur"},
                            {'type': 'password', 'name': 'mot_de_passe', 'message': 'Mot de passe :'}]

    def make_choice(self):
        answers = prompt(self.__questions)
        agent = SessionService().ouvrir_session(answers['nom_utilisateur'],answers['mot_de_passe'])
        if not (isinstance(agent, Agent)):
            #Ah ah ah... Vous n'avez pas dis le mot magique !
            print("Nom d'utilisateur ou mot de passe incorrect. Veuillez réessayer.")
            return ConnexionView()
        else:
            Session().agent = agent
            return MenuPrincipalView()
