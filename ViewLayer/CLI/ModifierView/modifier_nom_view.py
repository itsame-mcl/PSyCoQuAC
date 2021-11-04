from PyInquirer import prompt
from ViewLayer.CLI.session import Session
from DataLayer import DAO as dao
from ViewLayer.CLI.ModifierView.continuer_modif_view import ContinuerModifView

class ModifierNomView:

    def __init__(self) -> None:
        self.__questions = [{'type': 'input','name': 'nom','message': "Quel est votre nouveau nom ?"}]

    def modifier_nom(self, session: Session):
        answers = prompt(self.__questions)
        nouvel_agent = session.agent.nom = answers['nom']
        dao.DAOAgent.modifier_agent(nouvel_agent)
        return ContinuerModifView.continuer(session)