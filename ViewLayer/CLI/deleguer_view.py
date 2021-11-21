from typing import List
from PyInquirer import prompt
from BusinessLayer.BusinessObjects.gestionnaire import Gestionnaire
from BusinessLayer.BusinessObjects.superviseur import Superviseur
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.session import Session
from BusinessLayer.LocalServices.Gestion.agent_service import AgentService


class DeleguerView(AbstractView):
    def __init__(self) -> None:
        self.__equipe = AgentService().recuperer_equipe(Session().agent.agent_id)
        self.__equipe = [agent for agent in self.__equipe if isinstance(agent, Gestionnaire)]
        self.__delegues = AgentService().recuperer_liste_delegues(Session().agent.agent_id)
        self.__superviseurs = AgentService().recuperer_liste_superviseurs()
        self.__superviseurs = [superviseur for superviseur in self.__superviseurs if
                               superviseur.agent_id != Session().agent.agent_id]
        self.__questions = [{'type': 'list', 'name': 'choix', 'message': "Que voulez-vous faire ?",
                             'choices': ['D) Déléguer (temporairement) des gestionnaires',
                                         'T) Transférer (définitivement) des gestionnaires',
                                         'Q) Retourner au menu principal'],
                             'filter': lambda val: str.upper(val)[0]}]
        if len(self.__delegues) > 0:
            self.__questions[0]['choices'].insert(2, 'R) Rétrocéder des gestionnaires')

    @staticmethod
    def __prompt_gestionnaires(liste_gestionnaires: List[Gestionnaire]) -> list:
        choix_agents = [{'type': 'checkbox', 'name': 'ges', 'message': 'Quels gestionnaires sont '
                                                                       'concernés ?',
                         'choices': [], 'filter': lambda val: [int(row.split()[0]) for row in val],
                         'validate': lambda ans: "Vous devez choisir au moins un agent." if len(ans) == 0 else True}]
        for agent in liste_gestionnaires:
            choix_agents[0]['choices'].append({'name': str(agent.agent_id) + " - " +
                                               str(agent.prenom) + " " + str(agent.nom)})
        return choix_agents

    @staticmethod
    def __prompt_superviseur(liste_superviseurs: List[Superviseur]) -> list:
        choix_agent = [{'type': 'list', 'name': 'sup', 'message': 'A quel superviseur souhaitez vous '
                        'déléguer/transférer ?',
                        'choices': [], 'filter': lambda val: int(val.split()[0])}]
        for agent in liste_superviseurs:
            choix_agent[0]['choices'].append(str(agent.agent_id) + " - " + str(agent.prenom) + " " +
                                             str(agent.nom))
        return choix_agent

    def make_choice(self):
        answers = prompt(self.__questions)
        if answers['choix'] in ["D", "T"]:
            gestionnaires_a_modifier = prompt(self.__prompt_gestionnaires(self.__equipe))
            superviseur_delegue = prompt(self.__prompt_superviseur(self.__superviseurs))
            res = True
            for gestionnaire in gestionnaires_a_modifier['ges']:
                if answers['choix'] == "D":
                    new_res = AgentService().deleguer_agent(gestionnaire, superviseur_delegue['sup'])
                else:
                    new_res = AgentService().transferer_agent(gestionnaire, superviseur_delegue['sup'])
                res = res * new_res
        elif answers['choix'] == "R":
            gestionnaires_a_retroceder = prompt(self.__prompt_gestionnaires(self.__delegues))
            res = True
            for gestionnaire in gestionnaires_a_retroceder['ges']:
                new_res = AgentService().retroceder_agent(gestionnaire)
                res = res * new_res
        else:
            res = True
        return res
