from PyInquirer import prompt
from BusinessLayer.LocalServices.Gestion.session_service import SessionService
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.consulter_pot_agent import ConsulterPotView
from ViewLayer.CLI.gestion_equipe_view import GestionEquipeView
from ViewLayer.CLI.import_export_view import ImportExportView
from ViewLayer.CLI.modifier_agent_view import ModifierAgentView
from ViewLayer.CLI.repartir_view import RepartirView
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
                             'choices': ['P) Consulter mon pot', 'C) Contrôler des fiches', 'R) Reprendre des fiches',
                                         'M) Modifier mon compte']}]

    def make_choice(self):
        if Session().agent is None:
            return start.StartView()
        if Session().droits:
            self.__questions[0]['choices'].insert(0, "I) Importer/Exporter des lots")
            self.__questions[0]['choices'].insert(1, "F) Affecter des lots")
            self.__questions[0]['choices'].append("G) Gérer l'équipe et les agents")
        self.__questions[0]['choices'].append('Q) Me déconnecter')
        answers = prompt(self.__questions)
        if str.upper(answers['choix'][0]) == "P":
            return ConsulterPotView()
        if str.upper(answers['choix'][0]) == "C":
            return ConsulterPotView(controle=True, reprise=False)
        if str.upper(answers['choix'][0]) == "R":
            return ConsulterPotView(controle=False, reprise=True)
        if str.upper(answers['choix'][0]) == "M":
            return ModifierAgentView()
        if str.upper(answers['choix'][0]) == "Q":
            SessionService().fermer_session()
            return MenuPrincipalView()
        if str.upper(answers['choix'][0]) == "G":
            return GestionEquipeView()
        if str.upper(answers['choix'][0]) == "I":
            return ImportExportView()
        if str.upper(answers['choix'][0]) == "F":
            return RepartirView()
