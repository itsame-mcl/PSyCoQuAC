from PyInquirer import prompt
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.session import Session
from BusinessLayer.LocalServices.Gestion.agent_service import AgentService
from ViewLayer.CLI.menu import MenuPrincipalView


class DeleguerView(AbstractView):
    def __init__(self) -> None:
        self.__questions = [{'type': 'list', 'name': 'choix', 'message': "Que voulez-vous faire ?",
                             'choices': ['A) Déléguer un agent de votre équipe', 'B) Déléguer toute votre équipe',
                                         'C) Retourner au menu principal']}]
        self.__questions1 = [{'type': 'input', 'name': 'id_agent', 'message': 'Quel agent voulez-vous déléguer ?'}]
        self.__questions2 = [{'type': 'input', 'name': 'id_superviseur', 'message': 'À quel superviseur souhaitez-vous déléguer ?'}]

    def make_choice(self):
        answers = prompt(self.__questions)
        if 'a' in str.lower(answers['choix']):
            answers1 = prompt(self.__questions1)
            answers2 = prompt(self.__questions2)
            succes = AgentService().deleguer_agent(answers1['id_agent'], answers2['id_superviseur'])
            if not(succes):
                print("L'enregistrement a échoué. Veuillez réessayer ultérieurement.")
            return DeleguerView()
        if 'b' in str.lower(answers['choix']):
            answers2 = prompt(self.__questions2)
            succes = AgentService().deleguer_agent(Session().agent.agent_id, answers2['id_superviseur'])
            if not(succes):
                print("L'enregistrement a échoué. Veuillez réessayer ultérieurement.")
            return DeleguerView()
        else:
            return MenuPrincipalView()
