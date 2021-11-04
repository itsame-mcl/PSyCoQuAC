from PyInquirer import prompt
from ViewLayer.CLI.session import Session
from BusinessLayer.LocalServices.Gestion.fiche_agent_service import AgentServices
from ViewLayer.CLI.ModifierView.continuer_modif_view import ContinuerModifView

class ModifierPrenomView:

    def __init__(self) -> None:
        self.__questions = [{'type': 'input','name': 'prenom','message': "Quel est votre nouveau prénom ?"}]

    def modifier_prenom(self, session: Session):
        answers = prompt(self.__questions)
        nouvel_agent = session.agent.prenom = answers['prenom']
        probleme = AgentServices.modifier_agent(nouvel_agent)
        if not(probleme):
            print('La modification a échoué. Veuillez réessayer ultérieurement.')
        return ContinuerModifView(session)