from PyInquirer import prompt
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.session import Session
from ViewLayer.CLI.menu import MenuPrincipalView

class ImportExportView(AbstractView):

    def __init__(self, session : Session) -> None:
        self.__questions = [{'type': 'list','name': 'choix','message': 'Quelle opération souhaitez-vous effectuer ?',
                            'choices': ['1) Importation', '2) Exportation']}]

    def make_choice(self, session : Session):
        answers = prompt(self.__questions)
        if '1' in answers['choix']:
            from BusinessLayer.LocalServices.IO.importation_service import ImportationServices
            ImportationServices.importation
        else:
            from BusinessLayer.LocalServices.IO.exportation_service import ExportationServices
            ExportationServices.exportation
        return MenuPrincipalView(session)
