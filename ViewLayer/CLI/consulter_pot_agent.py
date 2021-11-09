from PyInquirer import prompt
from BusinessLayer.BusinessObjects.session import Session
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse

class ConsulterPotView:

    def __init__(self, session : Session) -> None:
        self.__questions = [{'type': 'input','name': 'choix','message': "De quel agent souhaitez-vous consulter le pot ?"}]
        self.__questions2 = [{'type': 'list','name': 'choix','message': 'Que voulez-vous faire ?',
                            'choices': ['p) Retourner à la fiche précédente', 's) Passer à la fiche suivante', 'm) Retourner au menu principal']}]

    def make_choice(self, session : Session):
        answers = prompt(self.__questions)
        pot = DAOFicheAdresse.recupere_pot(session.agent_id) 
        curseur = 0
        fiche = pot[curseur]
        print('Fiche adresse n°:' + str(fiche.fiche_id) + '\n   Données initiales :\nAdresse initiale : ' + str(fiche.adresse_initiale) + '\n   Données API :\nAdresse finale : '  + str(fiche.adresse_finale) + '\nCoordonnées GPS : ' + str(fiche.coords_wgs84))
        elif 'p' in str.lower(answers['choix']) :
            curseur = (curseur-1) % len(pot)
            return ControlerFiche(session, curseur)
        elif 's'in str.lower(answers['choix']) :
            curseur = (curseur+1) % len(pot)
            return ControlerFiche(session, curseur)
        elif 'm' in str.lower(answers['choix']) :
            return MenuPrincipalView(session)
        if 'q' in str.lower(answers['choix']):
            return None
        else:
            return ConnexionView()