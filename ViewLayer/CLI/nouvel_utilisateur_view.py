from PyInquirer import  prompt
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.menu import MenuPrincipalView
from ViewLayer.CLI.session import Session
from DataLayer.DAO.dao_agent import DAOAgent
from BusinessLayer.BusinessObjects.agent_factory import AgentFactory as factory


class NouvelUtilisateurView(AbstractView):
    def __init__(self, session : Session) -> None:
        self.__questions = [{'type': 'input','name': 'prenom','message': 'Prénom :'}, {'type': 'input','name': 'nom','message': 'NOM :'},
            {'type': 'input','name': 'est_superviseur','message': 'Rôle :'}, {'type': 'input','name': 'quotite','message': 'Quotité de travail :'},
            {'type': 'input','name': 'nom_utilisateur','message': "Nom d'utilisateur :"}, {'type': 'password','name': 'mot_de_passe','message': 'Mot de passe'}]

    def make_choice(self):
        answers = prompt(self.__questions)
        id_agent = DAOAgent.recuperer_prochain_id()
        nouvel_agent = factory.from_dict(answers)
        answers['identifiant']
        answers['identifiant_superviseur'] = self.__session.agent.agent_id
        probleme = DAOAgent.creer_agent(nouvel_agent, answers['nom_utilisateur'], answers['mot_de_passe'])
        if not(probleme):
            print("L'enregistrement du nouvel utilisateur a échoué. Veuillez réessayer ultérieurement.")
            return MenuPrincipalView()
        else:
            return MenuPrincipalView()
