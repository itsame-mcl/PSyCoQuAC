from PyInquirer import prompt
from ViewLayer.CLI.session import Session
from BusinessLayer.LocalServices.Gestion.agent_service import AgentService
from ViewLayer.CLI.ModifierView.continuer_modif_view import ContinuerModifView

class ModifierNomView:

    def __init__(self, session) -> None:
        self.__questions = [{'type': 'input','name': 'nom','message': "Quel est votre nouveau nom ?"}]

    def modifier_nom(self, session: Session):
        answers = prompt(self.__questions)
        session.agent.nom = answers['nom']
        probleme = AgentService.modifier_agent(session.agent.as_dict())
        if not(probleme):
            print('La modification a échoué. Veuillez réessayer ultérieurement.')
        return ContinuerModifView(session)