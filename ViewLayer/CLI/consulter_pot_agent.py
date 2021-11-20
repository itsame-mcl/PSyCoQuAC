from PyInquirer import prompt
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.session import Session
from BusinessLayer.LocalServices.TraitementFA.controle_reprise_service import ControleRepriseService
from ViewLayer.CLI.controler_view import ControlerView
from ViewLayer.CLI.reprendre_view import ReprendreView
import ViewLayer.CLI.menu as mp


class ConsulterPotView(AbstractView):
    def __init__(self, id_agent: int = None, controle: bool = True, reprise: bool = True, curseur: int = 0) -> None:
        if id_agent is None:
            self.__id_agent = Session().agent.agent_id
        else:
            self.__id_agent = id_agent
        self.pot = ControleRepriseService().consulter_pot_controle_reprise(self.__id_agent, controle, reprise)
        self.__curseur = curseur
        self.__questions = [{'type': 'list', 'name': 'choix', 'message': 'Que voulez-vous faire ?',
                             'choices': ['p) Retourner à la fiche précédente', 's) Passer à la fiche suivante',
                                         'm) Retourner au menu principal']}]
        self.__questions2 = [{'type': 'list', 'name': 'choix', 'message': 'Que voulez-vous faire ?',
                             'choices': ['p) Retourner à la fiche précédente', 's) Passer à la fiche suivante',
                                         'c) Controler/Reprendre la fiche', 'm) Retourner au menu principal']}]

    def display_info(self):
        if len(self.pot) > 0:
            self.__curseur = self.__curseur % len(self.pot)
            fiche = self.pot[self.__curseur]
            print(fiche)
        else:
            print("Le pot de fiches à traiter est vide.")

    def make_choice(self):
        if len(self.pot) > 0:
            fiche = self.pot[self.__curseur]
            if self.__id_agent == Session().agent.agent_id:
                answers = prompt(self.__questions2)
            else:
                answers = prompt(self.__questions)
            if 'p' in str.lower(answers['choix'][0]):
                self.__curseur = (self.__curseur - 1) % len(self.pot)
                return self
            elif 's' in str.lower(answers['choix'][0]):
                self.__curseur = (self.__curseur + 1) % len(self.pot)
                return self
            elif 'c' in str.lower(answers['choix'][0]):
                if fiche.code_res == "TC":
                    modal = ControlerView(self, fiche)
                elif fiche.code_res == "TR":
                    modal = ReprendreView(self, fiche)
                else:
                    return self
                modal.display_info()
                res, caller = modal.make_choice()
                if res:
                    caller.pot.remove(fiche)
                return caller
            else:
                return mp.MenuPrincipalView()
        else:
            return mp.MenuPrincipalView()
