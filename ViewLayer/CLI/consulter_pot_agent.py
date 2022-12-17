from PyInquirer import prompt
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.session import Session
from BusinessLayer.LocalServices.TraitementFA.controle_reprise_service import ControleRepriseService
from ViewLayer.CLI.controler_view import ControlerView
from ViewLayer.CLI.reprendre_view import ReprendreView
import ViewLayer.CLI.menu as mp


class ConsulterPotView(AbstractView):
    def __init__(self, id_agent: int = None, controle: bool = False, reprise: bool = False, curseur: int = 0,
                 caller: AbstractView = None) -> None:
        if id_agent is None:
            self.__id_agent = Session().agent.agent_id
        else:
            self.__id_agent = id_agent
        if controle or reprise:
            self.__delete_on_commit = True
            self.__pot = ControleRepriseService().consulter_pot_controle_reprise(self.__id_agent, controle, reprise)
        else:
            self.__delete_on_commit = False
            self.__pot = ControleRepriseService().consulter_pot(self.__id_agent)
        self.__curseur = curseur
        if caller is not None:
            self.__caller = caller
        else:
            self.__caller = mp.MenuPrincipalView()

    def display_info(self):
        if len(self.__pot) > 0:
            self.__curseur = self.__curseur % len(self.__pot)
            fiche = self.__pot[self.__curseur]
            print(fiche)
        else:
            print("Le pot de fiches à traiter est vide.")

    def make_choice(self):
        if len(self.__pot) > 0:
            fiche = self.__pot[self.__curseur]
            questions = [{'type': 'list', 'name': 'choix', 'message': 'Que voulez-vous faire ?', 'choices': []}]
            if len(self.__pot) > 1:
                questions[0]['choices'].append("P) Retourner à la fiche précédente")
                questions[0]['choices'].append("S) Passer à la fiche suivante")
            if self.__id_agent == Session().agent.agent_id:
                if fiche.code_res == "TC":
                    questions[0]['choices'].append("C) Contrôler la fiche")
                elif fiche.code_res == "TR":
                    questions[0]['choices'].append("R) Reprendre la fiche")
            questions[0]['choices'].append('Q) Retourner au menu principal')
            answers = prompt(questions)
            if str.upper(answers['choix'][0]) == "P":
                self.__curseur = (self.__curseur - 1) % len(self.__pot)
                return self
            if str.upper(answers['choix'][0]) == "S":
                self.__curseur = (self.__curseur + 1) % len(self.__pot)
                return self
            if str.upper(answers['choix'][0]) in ["C", "R"]:
                if fiche.code_res == "TC":
                    modal = ControlerView(fiche)
                elif fiche.code_res == "TR":
                    modal = ReprendreView(fiche)
                else:
                    return self
                modal.display_info()
                res, nouv_fiche = modal.make_choice()
                if res:
                    if self.__delete_on_commit:
                        self.__pot.remove(fiche)
                    else:
                        self.__pot[self.__pot.index(fiche)] = nouv_fiche
                else:
                    print("La sauvegarde a échoué. Veuillez réessayer ultérieurement.")
                return self
            if str.upper(answers['choix'][0]) == "Q":
                return self.__caller
            raise ValueError
        else:
            return self.__caller
