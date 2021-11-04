from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.session import Session
from ViewLayer.CLI.menu import MenuPrincipalView

class DeconnexionView(AbstractView):

    def __init__(self, session : Session) -> None:
        pass

    def make_choice(self, session : Session):
        print("Alors infidele, on s'en va sans dire au revoir ?")
        session.agent.agent_id = 0
        return MenuPrincipalView(session)