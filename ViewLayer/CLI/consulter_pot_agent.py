from PyInquirer import prompt
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse

class ConsulterPotView:

    def __init__(self, id_agent : int, curseur : int = 0) -> None:
        self.__questions = [{'type': 'list','name': 'choix','message': 'Que voulez-vous faire ?',
                            'choices': ['p) Retourner à la fiche précédente', 's) Passer à la fiche suivante', 'm) Retourner au menu principal']}]

    def make_choice(self):
        pot = DAOFicheAdresse.recupere_pot(ConsulterPotView.id_agent) 
        fiche = pot[ConsulterPotView.curseur]
        print('Fiche adresse n°' + str(fiche.fiche_id) + '\n   Données initiales :\nAdresse initiale : ' + str(fiche.adresse_initiale) + '\n   Données API :\nAdresse finale : '  + str(fiche.adresse_finale) + '\nCoordonnées GPS : ' + str(fiche.coords_wgs84))
        answers = prompt(self.__questions)
        if 'p' in str.lower(answers['choix']) :
            curseur = (ConsulterPotView.curseur-1) % len(pot)
            return ConsulterPotView(ConsulterPotView.id_agent, curseur)
        elif 's' in str.lower(answers['choix']) :
            curseur = (ConsulterPotView.curseur+1) % len(pot)
            return ConsulterPotView(ConsulterPotView.id_agent, curseur)
        else:
            from ViewLayer.CLI.menu import MenuPrincipalView
            return MenuPrincipalView()