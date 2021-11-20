from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from ViewLayer.CLI.abstract_view import AbstractView
from BusinessLayer.LocalServices.TraitementFA.controle_reprise_service import ControleRepriseService
from PyInquirer import prompt


class ControlerView(AbstractView):
    def __init__(self, caller: AbstractView, fiche: FicheAdresse) -> None:
        self.__caller = caller
        self.__fiche = fiche
        self.__questions = [{'type': 'list', 'name': 'choix', 'message': 'Comment qualifier les données de cette fiche ?',
                             'choices': ['C) Les données sont correctes', 'I) Les données sont incorrectes ',
                                         'Q) Décider plus tard']}]
        self.__questions2 = [
            {'type': 'list', 'name': 'choix', 'message': 'Confirmez-vous votre décision ?', 'choices': ['Oui', 'Non']}]

    def display_info(self):
        print(self.__fiche)

    def make_choice(self):
        answers = prompt(self.__questions)
        if str.upper(answers['choix'][0]) in ['C', 'I']:
            answers2 = prompt(self.__questions2)
            if str.upper(answers2['choix'][0]) == 'O':
                if str.upper(answers['choix'][0]) == 'C':
                    res = ControleRepriseService().validation_fiche(self.__fiche, True)
                else:
                    res = ControleRepriseService().validation_fiche(self.__fiche, True)
                return res, self.__caller
            elif str.upper(answers2['choix'][0]) == 'N':
                res = False
                return res, self.__caller
        elif str.upper(answers['choix'][0]) == 'Q':
            return False, self.__caller
        else:
            raise ValueError
