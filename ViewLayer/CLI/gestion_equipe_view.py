from PyInquirer import prompt
from BusinessLayer.LocalServices.Gestion.agent_service import AgentService
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.nouvel_utilisateur_view import NouvelUtilisateurView
from ViewLayer.CLI.modifier_agent_view import ModifierAgentView
from ViewLayer.CLI.consulter_pot_agent import ConsulterPotView
from ViewLayer.CLI.session import Session
import ViewLayer.CLI.menu as mp


class GestionEquipeView(AbstractView):
    def __init__(self) -> None:
        self.__questions = [{'type': 'list', 'name': 'choix', 'message': 'Que voulez-vous faire ?',
                             'choices': ["V) Consulter le pot d'un agent", "A) Ajouter un agent dans l'équipe",
                                         "S) Supprimer un agent de l'équipe", 'M) Modifier un agent',
                                         'Q) Retourner au menu principal']}]
        self.__questions2 = [{'type': 'input', 'name': 'id', 'message': "Quel est l'identifiant de l'agent ?"}]
        self.__questions3 = [{'type': 'list', 'name': 'choix', 'message': 'Souhaitez-vous faire autre chose ?',
                              'choices': ['O) Oui', 'N) Non']}]

    def make_choice(self):
        answers = prompt(self.__questions)
        if str.upper(answers['choix'][0]) == "V":
            answers2 = prompt(self.__questions2)
            return ConsulterPotView(int(answers2['id']))
        elif str.upper(answers['choix'][0]) == "A":
            succes = NouvelUtilisateurView().make_choice()
            if not(succes):
                print("L'ajout de l'agent a échoué. Veuillez réessayer ultérieurement.")
            answers3 = prompt(self.__questions3)
            if 'o' in str.lower(answers3['choix']):
                return GestionEquipeView()
            else:
                return mp.MenuPrincipalView()
        elif str.upper(answers['choix'][0]) == "S":
            answers2 = prompt(self.__questions2)
            succes = AgentService().supprimer_agent(answers2['id'])
            if not succes:
                print("La suppression de l'agent a échoué. Veuillez réessayer ultérieurement.")
            answers3 = prompt(self.__questions3)
            if 'o' in str.lower(answers3['choix']):
                return GestionEquipeView()
            else:
                return mp.MenuPrincipalView()
        elif str.upper(answers['choix'][0]) == "M":
            answers2 = prompt(self.__questions2)
            agent = AgentService().recuperer_agent(int(answers2['id']))
            view = ModifierAgentView(agent)
            view.display_info()
            view.make_choice()
            answers3 = prompt(self.__questions3)
            if 'o' in str.lower(answers3['choix']):
                return GestionEquipeView()
            else:
                return mp.MenuPrincipalView()
        else:
            return mp.MenuPrincipalView()
