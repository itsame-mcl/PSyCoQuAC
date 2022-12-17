from PyInquirer import prompt
from BusinessLayer.LocalServices.Gestion.agent_service import AgentService
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.session import Session


class NouvelUtilisateurView(AbstractView):
    def __init__(self, on_setup=False) -> None:
        self.__on_setup = on_setup
        self.__questions = [{'type': 'input', 'name': 'prenom', 'message': 'Prénom :'},
                            {'type': 'input', 'name': 'nom', 'message': 'Nom :'},
                            {'type': 'list', 'name': 'est_superviseur', 'message': 'Rôle :',
                             'choices': ["Gestionnaire", "Superviseur"], 'default': 'Gestionnaire',
                             'filter': self.__role_filter, 'when': lambda val: not on_setup},
                            {'type': 'input', 'name': 'quotite', 'message': 'Quotité de travail :',
                             'filter': float},
                            {'type': 'input', 'name': 'nom_utilisateur', 'message': "Nom d'utilisateur :"},
                            {'type': 'password', 'name': 'mot_de_passe', 'message': 'Mot de passe :'}]

    @staticmethod
    def __role_filter(val) -> bool:
        if val == "Gestionnaire":
            return False
        if val == "Superviseur":
            return True

    def make_choice(self):
        answers = prompt(self.__questions)
        if self.__on_setup:
            answers["est_superviseur"] = True
        if not (answers["est_superviseur"]):
            succes = AgentService().creer_agent(answers['est_superviseur'], answers['quotite'],
                                                answers['nom_utilisateur'], answers['mot_de_passe'],
                                                answers['prenom'], answers['nom'], Session().agent.agent_id)
        else:
            succes = AgentService().creer_agent(answers['est_superviseur'], answers['quotite'],
                                                answers['nom_utilisateur'], answers['mot_de_passe'],
                                                answers['prenom'], answers['nom'])
        return succes
