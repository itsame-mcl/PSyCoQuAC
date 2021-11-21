from PyInquirer import prompt
from BusinessLayer.LocalServices.Gestion.agent_service import AgentService
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.session import Session


class NouvelUtilisateurView(AbstractView):
    def __init__(self) -> None:
        self.__questions = [{'type': 'input', 'name': 'prenom', 'message': 'Prénom :'},
                            {'type': 'input', 'name': 'nom', 'message': 'Nom :'},
                            {'type': 'list', 'name': 'est_superviseur', 'message': 'Rôle :',
                             'choices': ["Gestionnaire", "Superviseur"], 'default': 'Gestionnaire',
                             'filter': lambda val: self.__role_filter(val)},
                            {'type': 'input', 'name': 'quotite', 'message': 'Quotité de travail :',
                             'filter': lambda val: float(val)},
                            {'type': 'input', 'name': 'nom_utilisateur', 'message': "Nom d'utilisateur :"},
                            {'type': 'password', 'name': 'mot_de_passe', 'message': 'Mot de passe :'}]

    def __role_filter(self, val) -> bool:
        if val == "Gestionnaire":
            return False
        elif val == "Superviseur":
            return True

    def make_choice(self):
        answers = prompt(self.__questions)
        if not (answers["est_superviseur"]):
            succes = AgentService().creer_agent(answers['est_superviseur'], answers['quotite'],
                                                answers['nom_utilisateur'], answers['mot_de_passe'],
                                            answers['prenom'], answers['nom'], Session().agent.agent_id)
        else:
            succes = AgentService().creer_agent(answers['est_superviseur'], answers['quotite'],
                                                answers['nom_utilisateur'], answers['mot_de_passe'],
                                                answers['prenom'], answers['nom'])
        return succes
