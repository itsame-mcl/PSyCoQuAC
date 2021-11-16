from pprint import pprint
from PyInquirer import  prompt
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.menu import MenuPrincipalView
from ViewLayer.CLI.session import Session
from DataLayer import DAO as dao
from BusinessLayer.BusinessObjects.agent_factory import AgentFactory as factory

class NouvelUtilisateurView(AbstractView):

    def __init__(self, session : Session) -> None:
        self.__questions = [{'type': 'input','name': 'prenom','message': 'Prénom :'}, {'type': 'input','name': 'nom','message': 'NOM :'},
            {'type': 'input','name': 'est_superviseur','message': 'Rôle :'}, {'type': 'input','name': 'quotite','message': 'Quotité de travail :'},
            {'type': 'input','name': 'nom_utilisateur','message': "Nom d'utilisateur :"}, {'type': 'password','name': 'mot_de_passe','message': 'Mot de passe'}]

    def make_choice(self, session : Session):
        answers = prompt(self.__questions)
        id_agent  = dao.DAOAgent.recuperer_prochain_id
        nouvel_agent = factory.from_dict(answers)
        answers['identifiant_superviseur'] = session.agent.agent_id
        probleme = dao.DAOAgent.creer_agent(nouvel_agent, answers['nom_utilisateur'], answers['mot_de_passe'])
        if not(probleme):
            print("L'enregistrement du nouvel utilisateur a échoué. Veuillez réessayer ultérieurement.")
            return MenuPrincipalView()
        else:
            return MenuPrincipalView()