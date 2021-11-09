from PyInquirer import prompt
from BusinessLayer.BusinessObjects.session import Session
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse

class ConsulterPotView:

    def __init__(self, id_agent : int, session : Session, curseur : int = 0) -> None:
        self.__questions = [{'type': 'list','name': 'choix','message': 'Que voulez-vous faire ?',
                            'choices': ['p) Retourner à la fiche précédente', 's) Passer à la fiche suivante', 'm) Retourner au menu principal']}]

    def make_choice(self, id_agent : int, session : Session, curseur : int = 0):
        pot = DAOFicheAdresse.recupere_pot(id_agent) 
        fiche = pot[curseur]
        print('Fiche adresse n°:' + str(fiche.fiche_id) + '\n   Données initiales :\nAdresse initiale : ' + str(fiche.adresse_initiale) + '\n   Données API :\nAdresse finale : '  + str(fiche.adresse_finale) + '\nCoordonnées GPS : ' + str(fiche.coords_wgs84))
        answers = prompt(self.__questions)
        if 'p' in str.lower(answers['choix']) :
            curseur = (curseur-1) % len(pot)
            return ConsulterPotView(id_agent, session, curseur)
        elif 's' in str.lower(answers['choix']) :
            curseur = (curseur+1) % len(pot)
            return ConsulterPotView(id_agent, session, curseur)
        else:
            from ViewLayer.CLI.menu import MenuPrincipalView
            return MenuPrincipalView(session)