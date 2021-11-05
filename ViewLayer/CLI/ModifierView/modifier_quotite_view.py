from PyInquirer import prompt
from ViewLayer.CLI.session import Session
from BusinessLayer.LocalServices.Gestion.agent_service import AgentService
from ViewLayer.CLI.ModifierView.continuer_modif_view import ContinuerModifView

class ModifierQuotiteView:

    def __init__(self) -> None:
        self.__questions = [{'type': 'input','name': 'quotite','message': "Quelle est votre nouvelle quotité de travail ?"}]

    def modifier_quotite(self, session: Session):
        answers = prompt(self.__questions)
        session.agent.quotite = answers['quotite']
        probleme = AgentService.modifier_agent(session.agent.as_dict())
        if not(probleme):
            print('La modification a échoué. Veuillez réessayer ultérieurement.')
        return ContinuerModifView(session)
            