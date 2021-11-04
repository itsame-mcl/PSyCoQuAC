from PyInquirer import prompt
from ViewLayer.CLI.session import Session
from BusinessLayer.LocalServices.Gestion.fiche_agent_service import AgentServices
from ViewLayer.CLI.ModifierView.continuer_modif_view import ContinuerModifView

class ModifierNomView:

    def __init__(self, session) -> None:
        self.__questions = [{'type': 'input','name': 'nom','message': "Quel est votre nouveau nom ?"}]

    def modifier_nom(self, session: Session):
        answers = prompt(self.__questions)
        nouvel_agent = session.agent.nom = answers['nom']
        probleme = AgentServices.modifier_agent(nouvel_agent)
        if not(probleme):
            print('La modification a échoué. Veuillez réessayer ultérieurement.')
        return ContinuerModifView(session)