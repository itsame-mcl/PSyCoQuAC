from BusinessLayer.LocalServices.Gestion.agent_service import AgentService
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.session import Session
from BusinessLayer.LocalServices.Gestion.statistique_service import StatistiqueService
import ViewLayer.CLI.menu as mp
from PyInquirer import prompt


class RepartirView(AbstractView):
    def __init__(self) -> None:
        self.__liste_lots = StatistiqueService().lots_a_affecter(Session().agent.agent_id)

    @staticmethod
    def __prompt_agents() -> list:
        equipe = AgentService().recuperer_equipe(Session().agent.agent_id)
        choix_agents = [{'type': 'checkbox', 'name': 'ids', 'message': 'A quels agents souhaitez-vous '
                                                                      'affecter des fiches ?',
                               'choices': [], 'filter': lambda val: [int(row.split()[0]) for row in val],
                         'validate': lambda ans: "Vous devez choisir au moins un agent." if len(ans) == 0 else True}]
        for agent in equipe:
            choix_agents[0]['choices'].append({'name': str(agent.agent_id) + " - " + str(agent.prenom) + " " +
                                                    str(agent.nom)})
        return choix_agents

    def make_choice(self):
        if len(self.__liste_lots) > 0:
            choices = list()
            for lot in self.__liste_lots:
                choices.append("Lot " + str(lot))
            choices.append("Q) Revenir au menu principal")
            choix_lot = [{'type': 'list', 'name': 'choix',
                          'message': "Quel lot souhaitez vous affecter ?",
                          'choices': choices}]
            answers_lot = prompt(choix_lot)
            if str.upper(answers_lot['choix'][0]) == "L":
                lot_selectionne = int(answers_lot['choix'].split()[1])
                choix_agents = prompt(self.__prompt_agents())
                agents_selectionnes = choix_agents["ids"]

                return RepartirView()
            elif str.upper(answers_lot['choix'][0]) == "Q":
                return mp.MenuPrincipalView()
            else:
                raise ValueError
        else:
            print("Vous n'avez aucun lot à affecter.")
            return mp.MenuPrincipalView()
