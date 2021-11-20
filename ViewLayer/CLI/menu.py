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
import ViewLayer.CLI.start_view as start
from ViewLayer.CLI.session import Session


class MenuPrincipalView(AbstractView):
    def __init__(self) -> None:
        if Session().agent is None:
            prenom = ""
        else:
            prenom = Session().agent.prenom
        self.__questions = [{'type': 'list', 'name': 'choix', 'message': 'Bonjour ' + prenom + ', que voulez-vous '
                                                                                               'faire ?',
                             'choices': ['P) Consulter son pot', 'C) Contrôler des fiches', 'R) Reprendre des fiches',
                                         'M) Modifier son compte']}]

    def make_choice(self):
        if Session().agent is None:
            return start.StartView()
        else:
            if Session().droits:
                self.__questions[0]['choices'].insert(0, "I) Importer/Exporter des lots")
                self.__questions[0]['choices'].insert(5, "T) Modifier le compte d'un agent")
                self.__questions[0]['choices'].insert(6, "D) Déleguer votre équipe/un agent")
                self.__questions[0]['choices'].insert(7, "U) Créer un nouvel utilisateur")
                self.__questions[0]['choices'].insert(8, "G) Gérer l'équipe")
            self.__questions[0]['choices'].append('Q) Se déconnecter')
            answers = prompt(self.__questions)
            if str.upper(answers['choix'][0]) == "P":
                return ConsulterPotView()
            elif str.upper(answers['choix'][0]) == "C":
                return ConsulterPotView(controle=True, reprise=False)
            elif str.upper(answers['choix'][0]) == "R":
                return ConsulterPotView(controle=False, reprise=True)
            elif str.upper(answers['choix'][0]) == "M":
                return ModifierView(Session().agent)
            elif str.upper(answers['choix'][0]) == "Q":
                return DeconnexionView()
            elif str.upper(answers['choix'][0]) == "T":
                choix_agent = prompt([{'type': 'input', 'name': 'agent',
                                       'message': "Quel est l'identifiant de l'agent ?"}])
                agent = AgentService().recuperer_agent(choix_agent['agent'][0])
                return ModifierView(agent)
            elif str.upper(answers['choix'][0]) == "D":
                return DeleguerView()
            elif str.upper(answers['choix'][0]) == "U":
                return NouvelUtilisateurView()
            elif str.upper(answers['choix'][0]) == "G":
                return GestionEquipeView()
            elif str.upper(answers['choix'][0]) == "I":
                return ImportExportView()
