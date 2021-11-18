from PyInquirer import prompt
from ViewLayer.CLI.abstract_view import AbstractView
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
from ViewLayer.CLI.session import Session


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
        self.__pot_vide = [{'type': 'list', 'name': 'choix', 'message': 'Que voulez-vous faire ?',
                            'choices': ['m) Retourner au menu principal']}]

    def make_choice(self):
        pot = DAOFicheAdresse().recuperer_pot(self.__id_agent)
        if len(pot) > 0:
            fiche = pot[self.__curseur]
            print('Fiche adresse n°' + str(fiche.fiche_id) + '\n   Données initiales :\nAdresse initiale : ' + str(
                fiche.adresse_initiale) + '\n   Données API :\nAdresse finale : ' + str(
                fiche.adresse_finale) + '\nCoordonnées GPS : ' + str(fiche.coords_wgs84))
            answers = prompt(self.__questions)
        else:
            print('Le pot est vide.')
            answers = prompt(self.__pot_vide)
        if 'p' in str.lower(answers['choix'][0]):
            curseur = (self.__curseur - 1) % len(pot)
            return ConsulterPotView(self.__id_agent, curseur)
        elif 's' in str.lower(answers['choix'][0]):
            curseur = (self.__curseur + 1) % len(pot)
            return ConsulterPotView(self.__id_agent, curseur)
        else:
            from ViewLayer.CLI.menu import MenuPrincipalView
            return MenuPrincipalView()
