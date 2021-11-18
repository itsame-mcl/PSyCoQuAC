from PyInquirer import prompt
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.menu import MenuPrincipalView
from ViewLayer.CLI.session import Session
from DataLayer.DAO.dao_agent import DAOAgent
import BusinessLayer.BusinessObjects.agent_factory as factory


class NouvelUtilisateurView(AbstractView):
    def __init__(self) -> None:
        self.__questions = [{'type': 'input', 'name': 'prenom', 'message': 'Prénom :'},
                            {'type': 'input', 'name': 'nom', 'message': 'NOM :'},
                            {'type': 'input', 'name': 'est_superviseur', 'message': 'Rôle :'},
                            {'type': 'input', 'name': 'quotite', 'message': 'Quotité de travail :'},
                            {'type': 'input', 'name': 'nom_utilisateur', 'message': "Nom d'utilisateur :"},
                            {'type': 'password', 'name': 'mot_de_passe', 'message': 'Mot de passe'}]

    def make_choice(self):
        answers = prompt(self.__questions)
        answers['identifiant_agent'] = DAOAgent().recuperer_dernier_id_agent() + 1
        if not (answers['est_superviseur']):
            answers['identifiant_superviseur'] = Session().agent.agent_id
        nouvel_agent = factory.AgentFactory.from_dict(answers)
        probleme = DAOAgent().creer_agent(nouvel_agent, answers['nom_utilisateur'], answers['mot_de_passe'])
        if not probleme:
            print("L'enregistrement du nouvel utilisateur a échoué. Veuillez réessayer ultérieurement.")
            return MenuPrincipalView()
        else:
            return MenuPrincipalView()
