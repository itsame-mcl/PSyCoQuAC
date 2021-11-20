from PyInquirer import prompt
from ViewLayer.CLI.abstract_view import AbstractView
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
from ViewLayer.CLI.session import Session
from BusinessLayer.LocalServices.TraitementFA.controle_reprise_service import ControleRepriseService
from ViewLayer.CLI.controle_view import ControlerView
from ViewLayer.CLI.reprendre_view import ReprendreView
import ViewLayer.CLI.menu as mp


class ConsulterPotView(AbstractView):
    def __init__(self, id_agent: int = None, curseur: int = 0) -> None:
        if id_agent is None:
            self.__id_agent = Session().agent.agent_id
        else:
            self.__id_agent = id_agent
        self.__curseur = curseur
        self.__questions = [{'type': 'list', 'name': 'choix', 'message': 'Que voulez-vous faire ?',
                             'choices': ['p) Retourner à la fiche précédente', 's) Passer à la fiche suivante',
                                         'm) Retourner au menu principal']}]
        self.__questions2 = [{'type': 'list', 'name': 'choix', 'message': 'Que voulez-vous faire ?',
                             'choices': ['p) Retourner à la fiche précédente', 's) Passer à la fiche suivante',
                                         'c) Controler/Reprendre la fiche', 'm) Retourner au menu principal']}]

    def display_info(self):
        pot = ControleRepriseService().consulter_pot(Session().agent.agent_id)
        if len(pot) > 0:
            fiche = pot[self.__curseur]
            print('Fiche adresse n°' + str(fiche.fiche_id) + 'Données initiales : adresse initiale : ' + 
                str(fiche.adresse_initiale) + 'Données API : Adresse finale : ' + str(fiche.adresse_finale) + 
                'Coordonnées GPS :' + str(fiche.coords_wgs84))
        else:
            print("Le pot est vide.")

    def make_choice(self):
        pot = DAOFicheAdresse().recuperer_pot(self.__id_agent)
        if len(pot) > 0:
            fiche = pot[self.__curseur]
            if self.__id_agent == Session().agent.agent_id:
                answers = prompt(self.__questions2)
            else:
                answers = prompt(self.__questions)
            if 'p' in str.lower(answers['choix'][0]):
                curseur = (self.__curseur - 1) % len(pot)
                return ConsulterPotView(self.__id_agent, curseur)
            elif 's' in str.lower(answers['choix'][0]):
                curseur = (self.__curseur + 1) % len(pot)
                return ConsulterPotView(self.__id_agent, curseur)
            elif 'c' in str.lower(answers['choix'][0]):
                if fiche.code_res == ['TC']:
                    return ControlerView(self.__curseur)
                elif fiche.code_res == ['TR']:
                    return ReprendreView(self.__curseur)
            else:
                return mp.MenuPrincipalView()
        else:
            return mp.MenuPrincipalView()
