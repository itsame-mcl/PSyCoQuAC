from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.session import Session
from ViewLayer.CLI.menu import MenuPrincipalView

class DeconnexionView(AbstractView):

    def __init__(self, session : Session) -> None:
        pass

    def display_info(self):
        print("Alors infidèle, on s'en va sans dire au revoir ?")

    def make_choice(self):
        Session().agent = None
        return MenuPrincipalView()
