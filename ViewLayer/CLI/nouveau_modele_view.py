from PyInquirer import prompt
from ast import literal_eval
from BusinessLayer.LocalServices.TraitementFA.modele_service import ModeleService
from ViewLayer.CLI.abstract_view import AbstractView
import pathlib


class NouveauModeleView(AbstractView):
    def __init__(self, path: str = None) -> None:
        nom_defaut = ""
        regex = ""
        if path is not None:
            path = pathlib.Path(path).name
            nom_defaut = "Modèle Ad-Hoc pour " + str(path)
            regex = str(path)
        self.__questions = [{'type': 'input', 'name': 'nom_modele', 'message': 'Comment souhaitez-vous '
                            'nommer ce modèle ?', 'default': nom_defaut},
                            {'type': 'input', 'name': 'regex',
                             'message': "Quelle chaîne permet d'activer ce modèle ? "
                                        "(vous pouvez utiliser les symboles classiques d'expressions régulières)",
                             'default': regex},
                            {'type': 'input', 'name': 'numero', 'message': "Dans quelles colonnes se trouvent les "
                            "informations relatives au numéro de l'adresse ? (vous pouvez saisir plusieurs valeurs "
                             "séparées par une virgule)",
                             'filter': lambda ans: self.__filter_champs(ans)},
                            {'type': 'input', 'name': 'voie', 'message': "Dans quelles colonnes se trouvent les "
                            "informations relatives au nom de la voie ? (vous pouvez saisir plusieurs valeurs "
                             "séparées par une virgule)",
                             'filter': lambda ans: self.__filter_champs(ans)},
                            {'type': 'input', 'name': 'cp', 'message': "Dans quelles colonnes se trouvent les "
                            "informations relatives au code postal ? (vous pouvez saisir plusieurs valeurs "
                             "séparées par une virgule)",
                             'filter': lambda ans: self.__filter_champs(ans)},
                            {'type': 'input', 'name': 'ville', 'message': "Dans quelles colonnes se trouvent les "
                            "informations relatives à la ville ? (vous pouvez saisir plusieurs valeurs "
                             "séparées par une virgule)",
                             'filter': lambda ans: self.__filter_champs(ans)}]
        self.__champs_sup = [{'type': 'confirm', 'name': 'continuer', 'message': 'Voulez vous ajouter un champ'
                             'supplémentaire ?', 'default': False}]
        self.__infos_sup = [{'type': 'input', 'name': 'nom_champ', 'message': 'Quel est le nom du champ '
                            'supplémentaire ?'},
                            {'type': 'input', 'name': 'position_champ', 'message': 'Quelle est la position de ce '
                            'champ ?', 'filter': lambda val: int(val) - 1}]

    @staticmethod
    def __filter_champs(ans_input):
        ans = []
        ast_input = literal_eval(str(ans_input))
        if isinstance(ast_input, int):
            ans.append(ast_input)
        else:
            ans = list(ast_input)
        ans = [val - 1 for val in ans]
        return ans

    def make_choice(self):
        answers = prompt(self.__questions)
        sup = {}
        ajouter_sup = True
        while ajouter_sup:
            reponse_sup = prompt(self.__champs_sup)
            if reponse_sup["continuer"]:
                infos_sup = prompt(self.__infos_sup)
                sup[infos_sup['nom_champ']] = infos_sup['position_champ']
            else:
                ajouter_sup = False
        succes = ModeleService().creer_modele(answers['nom_modele'], answers['regex'], answers['numero'],
                                              answers['voie'], answers['cp'], answers['ville'], sup)
        return succes
