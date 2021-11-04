from PyInquirer import prompt
from ViewLayer.CLI.session import Session
from DataLayer import DAO as dao
from ViewLayer.CLI.ModifierView.continuer_modif_view import ContinuerModifView

class ModifierPrenomView:

    def __init__(self) -> None:
        self.__questions = [{'type': 'input','name': 'prenom','message': "Quel est votre nouveau prénom ?"}]

    def modifier_prenom(self, session: Session):
        answers = prompt(self.__questions)
        nouvel_agent = session.agent.prenom = answers['prenom']
        dao.DAOAgent.modifier_agent(nouvel_agent)
        return ContinuerModifView.continuer(session)