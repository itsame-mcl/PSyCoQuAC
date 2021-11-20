from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.session import Session
from BusinessLayer.LocalServices.Gestion.statistique_service import StatistiqueService
import ViewLayer.CLI.menu as mp
from PyInquirer import prompt


class RepartirView(AbstractView):
    def __init__(self) -> None:
        self.__liste_lots = StatistiqueService().lots_a_affecter(Session().agent.agent_id)
        pass

    def display_info(self):
        pass

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
                return RepartirView()
            elif str.upper(answers_lot['choix'][0]) == "Q":
                return mp.MenuPrincipalView()
            else:
                raise ValueError
        else:
            print("Vous n'avez aucun lot à affecter.")
            return mp.MenuPrincipalView()
