from PyInquirer import prompt
from ViewLayer.CLI.abstract_view import AbstractView
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
                            'F) Créer un nouvel utilisateur', "G) Gestion de l'équipe", "H) Importer/Exporter des fichiers d'adresse"]}]
        self.__questions3 = [{'type': 'input', 'name': 'agent', 'message': "Quel est l'identifiant de l'agent ?"}]

    def make_choice(self):
        if Session().agent is None:
            from ViewLayer.CLI.start_view import StartView
            return StartView()
        else:
            if Session().droits:
                answers = prompt(self.__questions2)
            else:
                answers = prompt(self.__questions)
            print(answers)
            if 'A' in str.upper(answers['choix'][0]):
                from ViewLayer.CLI.consulter_pot_agent import ConsulterPotView
                return ConsulterPotView()
            elif 'B' in str.upper(answers['choix'][0]):
                from ViewLayer.CLI.modifier_view import ModifierView
                return ModifierView()
            elif 'C' in str.upper(answers['choix'][0]):
                from ViewLayer.CLI.deconnexion_view import DeconnexionView
                return DeconnexionView()
            elif 'D' in str.upper(answers['choix'][0]):
                from ViewLayer.CLI.deleguer_view import DeleguerView
                return DeleguerView()
            elif 'E' in str.upper(answers['choix'][0]):
                answers3 = prompt(self.__questions3)
                from BusinessLayer.LocalServices.Gestion.agent_service import AgentService
                agent = AgentService.recuperer_agent(answers3['agent'][0])
                from ViewLayer.CLI.modifier_view import ModifierView
                return ModifierView()
            elif 'F' in str.upper(answers['choix'][0]):
                from ViewLayer.CLI.nouvel_utilisateur_view import NouvelUtilisateurView
                return NouvelUtilisateurView()
            elif 'G' in str.upper(answers['choix'][0]):
                from ViewLayer.CLI.gestion_equipe_view import GestionEquipeView
                return GestionEquipeView()
            elif 'H' in str.upper(answers['choix'][0]):
                from ViewLayer.CLI.import_export_view import ImportExportView
                return ImportExportView()
            elif 'I' in str.upper(answers['choix'][0]):
                from ViewLayer.CLI.controle_view import ControlerView
                return ControlerView()
            elif 'J' in str.upper(answers['choix'][0]):
                from ViewLayer.CLI.reprendre_view import ReprendreView
                return ReprendreView()
