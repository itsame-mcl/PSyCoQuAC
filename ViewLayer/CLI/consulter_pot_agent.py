from PyInquirer import prompt
from ViewLayer.CLI.session import Session
from ViewLayer.CLI.abstract_view import AbstractView
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse


class ConsulterPotView(AbstractView):

    def __init__(self, curseur : int = 0) -> None:
        self.__curseur = curseur
        self.__questions = [{'type': 'list','name': 'choix','message': 'Que voulez-vous faire ?',
                            'choices': ['p) Retourner à la fiche précédente', 's) Passer à la fiche suivante', 'm) Retourner au menu principal']}]

    def make_choice(self):
        pot = DAOFicheAdresse().recuperer_pot(Session().agent.id_agent)
        fiche = pot[self.__curseur]
        print('Fiche adresse n°' + str(fiche.fiche_id) + '\n   Données initiales :\nAdresse initiale : ' + str(fiche.adresse_initiale) + '\n   Données API :\nAdresse finale : '  + str(fiche.adresse_finale) + '\nCoordonnées GPS : ' + str(fiche.coords_wgs84))
        answers = prompt(self.__questions)
        if 'p' in str.lower(answers['choix']) :
            curseur = (self.__curseur-1) % len(pot)
            return ConsulterPotView(curseur)
        elif 's' in str.lower(answers['choix']) :
            curseur = (self.__curseur+1) % len(pot)
            return ConsulterPotView(curseur)
        else:
            from ViewLayer.CLI.menu import MenuPrincipalView
            return MenuPrincipalView()