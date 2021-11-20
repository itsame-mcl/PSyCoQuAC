from PyInquirer import prompt
from BusinessLayer.LocalServices.IO.importation_service import ImportationService
from BusinessLayer.LocalServices.IO.exportation_service import ExportationService
from BusinessLayer.LocalServices.TraitementFA.modele_service import ModeleService
from BusinessLayer.WebServices.BANClient import BANClient
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.session import Session
import ViewLayer.CLI.menu as mp


class ImportExportView(AbstractView):
    def __init__(self) -> None:
        self.__questions = [{'type': 'list', 'name': 'choix', 'message': 'Quelle opération souhaitez-vous effectuer ?',
                             'choices': ['I) Importer un lot', 'X) Exportation']}]
        self.__import = [{'type': 'input', 'name': 'chemin', 'message': 'Quel est le chemin du fichier à importer ?'}]
        self.__id_export = [{'type': 'input', 'name': 'id', 'message': "Quel est l'identifiant du lot à exporter ?"}]
        self.__export = [{'type': 'input', 'name': 'chemin', 'message': 'Quel est la destination du lot à exporter ?'}]
        self.__validation_modele = [{'type': 'list', 'name': 'choix',
                                     'message': "Souhaitez-vous utiliser ce modèle pour l'importation ?",
                                     'choices': ["O) Oui, lancer l'importation", "N) Non, créer un nouveau modèle",
                                                 "Q) Non, abandonner l'importation"]}]
        self.__appel_api = [{'type': 'list', 'name': 'choix',
                             'message': "Souhaitez-vous soumettre maintenant ce lot à l'API BAN ?",
                             'choices': ["O) Oui", "N) Non"]}]

    def __importation(self):
        answers_import = prompt(self.__import)
        modele = ModeleService().identifier_modele(answers_import['chemin'])
        print(modele)
        answers_modele = prompt(self.__validation_modele)
        if str.upper(answers_modele['choix'][0]) == 'O':
            lot, res = ImportationService().importer_lot(Session().agent.agent_id, answers_import['chemin'], modele)
            if res:
                print("Lot numéro " + str(lot) + " importé avec succès !")
                answers_api = prompt(self.__appel_api)
                if str.upper(answers_api['choix'][0]) == 'O':
                    BANClient().geocodage_par_lot(lot, verbose=True)
                    return ImportExportView()
        elif str.upper(answers_modele['choix'][0]) == 'N':
            raise NotImplementedError
        elif str.upper(answers_modele['choix'][0]) == 'Q':
            return ImportExportView()
        else:
            raise ValueError

    def make_choice(self):
        answers = prompt(self.__questions)
        if str.upper(answers['choix'][0]) == 'I':
            self.__importation()
        else:
            answers_id = prompt(self.__id_export)
            answers_export = prompt(self.__export)
            ExportationService.exporter_lot(answers_id['id'][0], answers_export['chemin'][0])
        return mp.MenuPrincipalView()
