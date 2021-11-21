from PyInquirer import prompt
from BusinessLayer.LocalServices.Gestion.agent_service import AgentService
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.deleguer_view import DeleguerView
from ViewLayer.CLI.nouvel_utilisateur_view import NouvelUtilisateurView
from ViewLayer.CLI.modifier_agent_view import ModifierAgentView
from ViewLayer.CLI.consulter_pot_agent import ConsulterPotView
from ViewLayer.CLI.session import Session
import ViewLayer.CLI.menu as mp


class GestionEquipeView(AbstractView):
    def __init__(self) -> None:
        self.__questions = [{'type': 'list', 'name': 'choix', 'message': 'Que voulez-vous faire ?',
                             'choices': ["V) Consulter le pot d'un agent", "A) Créer un nouvel agent",
                                         "S) Supprimer un agent", 'M) Modifier un agent',
                                         "D) Déleguer l'équipe/un agent", 'Q) Retourner au menu principal'],
                             'filter': lambda val: str.upper(val)[0]}]
        self.__continue = [{'type': 'list', 'name': 'choix', 'message': 'Souhaitez-vous faire autre chose ?',
                            'choices': ['O) Oui', 'N) Non'], 'filter': lambda val: str.upper(val)[0]}]

    @staticmethod
    def __prompt_agent() -> list:
        equipe = AgentService().recuperer_equipe(Session().agent.agent_id)
        choix_agent = [{'type': 'list', 'name': 'id', 'message': 'Choisissez un agent de votre équipe :',
                        'choices': [], 'filter': lambda val: int(val.split()[0])}]
        for agent in equipe:
            choix_agent[0]['choices'].append(str(agent.agent_id) + " - " + str(agent.prenom) + " " +
                                             str(agent.nom))
        return choix_agent

    def make_choice(self):
        continuer = True
        while continuer:
            answers = prompt(self.__questions)
            if answers['choix'] == "Q":
                continuer = False
            else:
                if answers['choix'] == "V":
                    id_agent = prompt(self.__prompt_agent())
                    return ConsulterPotView(id_agent['id'], caller=self)
                elif answers['choix'] == "A":
                    succes = NouvelUtilisateurView().make_choice()
                    if not succes:
                        print("L'ajout de l'agent a échoué. Veuillez réessayer ultérieurement.")
                elif answers['choix'] == "S":
                    id_agent = prompt(self.__prompt_agent())
                    succes = AgentService().supprimer_agent(id_agent['id'])
                    if not succes:
                        print("La suppression de l'agent a échoué. Veuillez réessayer ultérieurement.")
                elif answers['choix'] == "M":
                    id_agent = prompt(self.__prompt_agent())
                    agent = AgentService().recuperer_agent(id_agent['id'])
                    view = ModifierAgentView(agent)
                    view.display_info()
                    view.make_choice()
                elif answers['choix'] == "D":
                    succes = DeleguerView().make_choice()
                    if not succes:
                        print("L'opération de délégation a échoué. Veuillez réessayer ultérieurement.")
                answer_continue = prompt(self.__continue)
                if answer_continue['choix'] == "O":
                    continuer = True
                else:
                    continuer = False
        return mp.MenuPrincipalView()
