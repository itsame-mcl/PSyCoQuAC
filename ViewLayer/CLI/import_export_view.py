from PyInquirer import prompt
from BusinessLayer.LocalServices.IO.importation_service import ImportationService
from BusinessLayer.LocalServices.IO.exportation_service import ExportationService
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.menu import MenuPrincipalView
from ViewLayer.CLI.session import Session


class ImportExportView(AbstractView):
    def __init__(self) -> None:
        self.__questions = [{'type': 'list', 'name': 'choix', 'message': 'Quelle opération souhaitez-vous effectuer ?',
                            'choices': ['1) Importation', '2) Exportation']}]
        self.__import = [{'type': 'input', 'name': 'chemin', 'message' : 'Quel est le chemin du fichier à importer ?'}]
        self.__id_export = [{'type': 'input', 'name': 'id', 'message' : "Quel est l'identifiant du lot à exporter ?"}]
        self.__export = [{'type': 'input', 'name': 'chemin', 'message' : 'Quel est la destination du lot à exporter ?'}]


    def make_choice(self):
        answers = prompt(self.__questions)
        if '1' in answers['choix']:
            answers_import = prompt(self.__import)
            ImportationService.importer_lot(Session.agent.agent_id, answers_import['chemin'][0])
        else:
            answers_id = prompt(self.__id_export)
            answers_export = prompt(self.__export)
            ExportationService.exporter_lot(answers_id['id'][0], answers_export['chemin'][0])
        return MenuPrincipalView()
