from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.connexion_view import ConnexionView
from ViewLayer.CLI.nouvel_utilisateur_view import NouvelUtilisateurView
from BusinessLayer.LocalServices.Gestion.agent_service import AgentService
from PyInquirer import prompt


class StartView(AbstractView):
    def __init__(self):
        nb_agents_en_base = len(AgentService().recuperer_equipe(0))
        if nb_agents_en_base == 0:
            self.__creer_agent = True
        else:
            self.__creer_agent = False
        self.__questions = [{'type': 'list','name': 'choix','message': 'Que voulez-vous faire ?',
                            'choices': ['C) Se connecter', "Q) Quitter l'application"]}]

    def make_choice(self):
        if self.__creer_agent:
            print("Création du premier superviseur :")
            succes = NouvelUtilisateurView(on_setup=True).make_choice()
            self.__creer_agent = not succes
            return self
        answers = prompt(self.__questions)
        if 'q' in str.lower(answers['choix']):
            return None
        return ConnexionView()
