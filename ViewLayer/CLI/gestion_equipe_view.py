from PyInquirer import prompt
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.session import Session

class GestionEquipeView(AbstractView):

    def __init__(self, session : Session) -> None:
        self.__questions = [{'type': 'list','name': 'choix','message': 'Que voulez-vous faire ?',
                            'choices': ["1) Consulter le pot d'un agent", "2) Ajouter un agent dans l'équipe", "3) Supprimer un agent de l'équipe", '4) Promouvoir un agent']}]
        self.__questions2 = [{'type': 'input','name': 'id','message': "Quel est l'identifiant de l'agent ?"}]

    def make_choice(self, session : Session):
        answers = prompt(self.__questions)
        if '1' in answers['choix']:
            answers2 = prompt(self.__questions2)
            from ViewLayer.CLI.consulter_pot_agent import ConsulterPotView
            return ConsulterPotView(int(answers2['id']), session)
        elif '2' in answers['choix']:
            answers2 = prompt(self.__questions2)
            from BusinessLayer.LocalServices.Gestion.agent_service import AgentService
            probleme = AgentService.ajout_agent_equipe(session.utilisateur_connecte.agent_id, answers2['id'])
            if not(probleme):
                print("L'enregistrement a échoué. Veuillez réessayer ultérieurement.")
            from ViewLayer.CLI.menu import MenuPrincipalView
            return MenuPrincipalView(session)
        elif '3' in answers['choix']:
            answers2 = prompt(self.__questions2)
            from BusinessLayer.LocalServices.Gestion.agent_service import AgentService
            probleme = AgentService.supprimer_agent(answers2['id'])
            if not(probleme):
                print("L'enregistrement a échoué. Veuillez réessayer ultérieurement.")
            from ViewLayer.CLI.menu import MenuPrincipalView
            return MenuPrincipalView(session)
        elif '4' in answers['choix']:
            answers2 = prompt(self.__questions2)
            from BusinessLayer.LocalServices.Gestion.agent_service import AgentService
            probleme = AgentService.promouvoir_agent(session.utilisateur_connecte.agent_id, answers2['id'])
            if not(probleme):
                print("L'enregistrement a échoué. Veuillez réessayer ultérieurement.")
            from ViewLayer.CLI.menu import MenuPrincipalView
            return MenuPrincipalView(session)
        else:
            from ViewLayer.CLI.menu import MenuPrincipalView
            return MenuPrincipalView(session)