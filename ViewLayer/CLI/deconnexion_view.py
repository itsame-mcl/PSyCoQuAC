from ViewLayer.CLI.session import Session
from ViewLayer.CLI.menu import MenuPrincipalView

class DeconnexionView:

    def __init__(self, session : Session) -> None:
        pass

    def deconnexion(self, session : Session):
        print("Alors infidele, on s'en va sans dire au revoir ?")
        session.agent.agent_id = 0
        return MenuPrincipalView.naviguer(session)