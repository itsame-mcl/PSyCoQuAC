from PyInquirer import prompt
from BusinessLayer.LocalServices.Gestion.agent_service import AgentService
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.consulter_pot_agent import ConsulterPotView
from ViewLayer.CLI.deconnexion_view import DeconnexionView
from ViewLayer.CLI.deleguer_view import DeleguerView
from ViewLayer.CLI.gestion_equipe_view import GestionEquipeView
from ViewLayer.CLI.import_export_view import ImportExportView
from ViewLayer.CLI.modifier_view import ModifierView
from ViewLayer.CLI.nouvel_utilisateur_view import NouvelUtilisateurView
from ViewLayer.CLI.start_view import StartView
from ViewLayer.CLI.session import Session


class MenuPrincipalView(AbstractView):
    def __init__(self) -> None:
        if Session().agent is None:
            prenom = ""
        else:
            prenom = Session().agent.prenom
        self.__questions = [{'type': 'list', 'name': 'choix', 'message': 'Bonjour ' + prenom + ', que voulez-vous faire ?',
                            'choices': ['A) Consulter son pot', 'B) Modifier son compte', 'C) Se déconnecter',
                            'I) Contrôler une fiche', 'J) Reprendre  une fiche']}]
        self.__questions2 = [{'type': 'list', 'name': 'choix', 'message': 'Bonjour ' + prenom + ', que voulez-vous faire ?',
                            'choices': ['A) Consulter son pot', 'B) Modifier son compte', 'C) Se déconnecter',
                            'D) Déleguer votre équipe/un agent', "E) Modifier le compte d'un agent",
                            'F) Créer un nouvel utilisateur', "G) Gestion de l'équipe", "H) Importer/Exporter des fichiers d'adresse",
                            'I) Contrôler une fiche', 'J) Reprendre  une fiche']}]
        self.__questions3 = [{'type': 'input', 'name': 'agent', 'message': "Quel est l'identifiant de l'agent ?"}]

    def make_choice(self):
        if Session().agent is None:
            return StartView()
        else:
            if Session().droits:
                answers = prompt(self.__questions2)
            else:
                answers = prompt(self.__questions)
            print(answers)
            if 'A' in str.upper(answers['choix'][0]):
                return ConsulterPotView()
            elif 'B' in str.upper(answers['choix'][0]):
                return ModifierView(Session().agent)
            elif 'C' in str.upper(answers['choix'][0]):
                return DeconnexionView()
            elif 'D' in str.upper(answers['choix'][0]):
                return DeleguerView()
            elif 'E' in str.upper(answers['choix'][0]):
                answers3 = prompt(self.__questions3)
                agent = AgentService.recuperer_agent(answers3['agent'][0])
                return ModifierView(agent)
            elif 'F' in str.upper(answers['choix'][0]):
                return NouvelUtilisateurView()
            elif 'G' in str.upper(answers['choix'][0]):
                return GestionEquipeView()
            elif 'H' in str.upper(answers['choix'][0]):
                return ImportExportView()
            elif 'I' in str.upper(answers['choix'][0]):
                return ConsulterPotView(controle=True, reprise=False)
            elif 'J' in str.upper(answers['choix'][0]):
                return ConsulterPotView(controle=False, reprise=True)
