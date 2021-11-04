from PyInquirer import prompt
from ViewLayer.CLI.session import Session
from DataLayer import DAO as dao
from ViewLayer.CLI.ModifierView.continuer_modif_view import ContinuerModifView

class ModifierQuotiteView:

    def __init__(self) -> None:
        self.__questions = [{'type': 'input','name': 'quotite','message': "Quelle est votre nouvelle quotité de travail ?"}]

    def modifier_quotite(self, session: Session):
        answers = prompt(self.__questions)
        nouvel_agent = session.agent.quotite = answers['quotite']
        dao.DAOAgent.modifier_agent(nouvel_agent)
        return ContinuerModifView.continuer(session)
            