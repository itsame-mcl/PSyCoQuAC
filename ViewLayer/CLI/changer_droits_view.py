from PyInquirer import prompt
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.menu import MenuPrincipalView
from ViewLayer.CLI.session import Session
from DataLayer import DAO as dao

class ChangerDroitsView(AbstractView):

    def __init__(self, session) -> None:
        self.__questions = [{'type': 'input','name': 'id_agent','message': "La loi, c'est toi ! De quel agent souhaitez-vous changer les droits ?"}]

    def make_choice(self, session : Session):
        answers = prompt(self.__questions)
        agent = dao.DAOAgent.recuperer_agent(answers['id_agent'])
        probleme = dao.DAOAgent.changer_droits(agent)
        if not(probleme):
            print("L'enregistrement a échoué. Veuillez réessayer.")
            return MenuPrincipalView.naviguer(session)
        