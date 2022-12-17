from PyInquirer import prompt
from BusinessLayer.LocalServices.IO.importation_service import ImportationService
from BusinessLayer.LocalServices.IO.exportation_service import ExportationService
from BusinessLayer.LocalServices.TraitementFA.modele_service import ModeleService
from BusinessLayer.LocalServices.Gestion.statistique_service import StatistiqueService
from ViewLayer.CLI.nouveau_modele_view import NouveauModeleView
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.session import Session
import ViewLayer.CLI.menu as mp


class ImportExportView(AbstractView):
    def __init__(self) -> None:
        self.__questions = [{'type': 'list', 'name': 'choix', 'message': 'Quelle opération souhaitez-vous effectuer ?',
                             'choices': ['I) Importer un lot', "A) Traiter un lot avec l'API BAN",
                                         'X) Exporter un lot', "Q) Revenir au menu principal"]}]
        self.__import = [{'type': 'input', 'name': 'chemin', 'message': 'Quel est le chemin du fichier à importer ?'}]
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
        modele_a_valider = True
        while modele_a_valider:
            modele = ModeleService().identifier_modele(answers_import['chemin'])
            print(modele)
            answers_modele = prompt(self.__validation_modele)
            if str.upper(answers_modele['choix'][0]) == 'O':
                modele_a_valider = False
                lot, res = ImportationService().importer_lot(Session().agent.agent_id, answers_import['chemin'], modele)
                if res:
                    print("Lot numéro " + str(lot) + " importé avec succès !")
                    self.__traitement_api(lot)
            elif str.upper(answers_modele['choix'][0]) == 'N':
                res = NouveauModeleView(answers_import['chemin']).make_choice()
                if not res:
                    print("Erreur lors de la création du modèle.")
            elif str.upper(answers_modele['choix'][0]) == 'Q':
                modele_a_valider = False
            else:
                raise ValueError

    def __traitement_api(self, id_lot):
        answers_api = prompt(self.__appel_api)
        if str.upper(answers_api['choix'][0]) == 'O':
            ImportationService().traiter_lot_api(id_lot, verbose=True)

    def make_choice(self):
        answers = prompt(self.__questions)
        if str.upper(answers['choix'][0]) == 'I':
            self.__importation()
            return ImportExportView()
        if str.upper(answers['choix'][0]) == 'A':
            liste_lots = ImportationService().lots_a_traiter_api(Session().agent.agent_id)
            if len(liste_lots) > 0:
                choices = []
                for lot in liste_lots:
                    choices.append("Lot " + str(lot))
                choices.append("Annuler")
                choix_lot = [{'type': 'list', 'name': 'choix',
                              'message': "Quel lot souhaitez vous traiter ?",
                              'choices': choices}]
                answers_lot = prompt(choix_lot)
                if str.upper(answers_lot['choix'][0]) == "L":
                    lot_selectionne = int(answers_lot['choix'].split()[1])
                    self.__traitement_api(lot_selectionne)
                elif str.upper(answers_lot['choix'][0]) == "A":
                    pass
                else:
                    raise ValueError
            else:
                print("Tous les lots que vous avez importés ont déjà été traités par l'API.")
            return ImportExportView()
        if str.upper(answers['choix'][0]) == 'X':
            liste_lots = StatistiqueService().fiches_par_lot()
            if len(liste_lots) > 0:
                choices = []
                for ligne in liste_lots:
                    choices.append("Lot " + str(ligne[0]) + " - " + str(ligne[1]) + " adresses")
                choices.append("Annuler")
                choix_lot = [{'type': 'list', 'name': 'choix',
                              'message': "Quel lot souhaitez vous traiter ?",
                              'choices': choices}]
                answers_lot = prompt(choix_lot)
                if str.upper(answers_lot['choix'][0]) == "L":
                    lot_selectionne = int(answers_lot['choix'].split()[1])
                    destination = prompt(self.__export)
                    ExportationService().exporter_lot(lot_selectionne, destination['chemin'])
                elif str.upper(answers_lot['choix'][0]) == "A":
                    pass
                else:
                    raise ValueError
            else:
                print("Aucun lot n'est disponible pour l'exportation.")
            return ImportExportView()
        if str.upper(answers['choix'][0]) == 'Q':
            return mp.MenuPrincipalView()
        raise ValueError
