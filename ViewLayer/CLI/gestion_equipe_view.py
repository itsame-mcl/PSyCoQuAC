from PyInquirer import prompt
from BusinessLayer.LocalServices.Gestion.agent_service import AgentService
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.modifier_view import ModifierView
from ViewLayer.CLI.consulter_pot_agent import ConsulterPotView
from ViewLayer.CLI.session import Session
import ViewLayer.CLI.menu as mp


class GestionEquipeView(AbstractView):
    def __init__(self) -> None:
        self.__questions = [{'type': 'list', 'name': 'choix', 'message': 'Que voulez-vous faire ?',
                             'choices': ["1) Consulter le pot d'un agent", "2) Ajouter un agent dans l'équipe",
                                         "3) Supprimer un agent de l'équipe", '4) Modifier un agent',
                                         '5) Retourner au menu principal']}]
        self.__questions2 = [{'type': 'input', 'name': 'id', 'message': "Quel est l'identifiant de l'agent ?"}]
        self.__questions3 = [{'type': 'list', 'name': 'choix', 'message': 'Souhaitez-vous faire autre chose ?',
                              'choices': ['O) Oui', 'N) Non']}]

    def make_choice(self):
        answers = prompt(self.__questions)
        if '1' in answers['choix']:
            answers2 = prompt(self.__questions2)
            return ConsulterPotView(int(answers2['id']))
        elif '2' in answers['choix']:
            answers2 = prompt(self.__questions2)
            succes = AgentService().ajout_agent_equipe(Session().agent.agent_id, answers2['id'])
            if not(succes):
                print("L'ajout de l'agent a échoué. Veuillez réessayer ultérieurement.")
            answers3 = prompt(self.__questions3)
            if 'o' in str.lower(answers3['choix']):
                return GestionEquipeView()
            else:
                return mp.MenuPrincipalView()
        elif '3' in answers['choix']:
            answers2 = prompt(self.__questions2)
            succes = AgentService().supprimer_agent(answers2['id'])
            if not succes:
                print("La suppression de l'agent a échoué. Veuillez réessayer ultérieurement.")
            answers3 = prompt(self.__questions3)
            if 'o' in str.lower(answers3['choix']):
                return GestionEquipeView()
            else:
                return mp.MenuPrincipalView()
        elif '4' in answers['choix']:
            answers2 = prompt(self.__questions2)
            agent = AgentService().recuperer_agent(int(answers2['id']))
            view = ModifierView(agent)
            view.display_info()
            view.make_choice()
            answers3 = prompt(self.__questions3)
            if 'o' in str.lower(answers3['choix']):
                return GestionEquipeView()
            else:
                return mp.MenuPrincipalView()
        else:
            return mp.MenuPrincipalView()
