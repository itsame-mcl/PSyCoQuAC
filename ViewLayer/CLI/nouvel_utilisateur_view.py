from PyInquirer import prompt
from BusinessLayer.LocalServices.Gestion.agent_service import AgentService
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.session import Session
from ViewLayer.CLI.menu import MenuPrincipalView


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
        if not(answers['est_superviseur']):
            answers['identifiant_superviseur'] = Session().agent.agent_id
        succes = AgentService().creer_agent(answers['est_superviseur'], answers['quotite'], answers['identifiant_superviseur'],
                                            answers['nom_utilisateur'], answers['mot_de_passe'], answers['prenom'], answers['nom'])
        if not(succes):
            print("L'enregistrement du nouvel utilisateur a échoué. Veuillez réessayer ultérieurement.")
        return MenuPrincipalView()
