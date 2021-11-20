from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from ViewLayer.CLI.abstract_view import AbstractView
from BusinessLayer.LocalServices.TraitementFA.controle_reprise_service import ControleRepriseService
from PyInquirer import prompt
import ViewLayer.CLI.menu as mp


class ControlerView(AbstractView):
    def __init__(self, caller: AbstractView, fiche: FicheAdresse) -> None:
        self.__caller = caller
        self.__fiche = fiche
        self.__questions = [{'type': 'list', 'name': 'choix', 'message': 'Comment qualifier les données de cette fiche ?',
                             'choices': ['C) Les données sont correctes', 'I) Les données sont incorrectes ',
                                         'A) Décider plus tard']}]
        self.__questions2 = [
            {'type': 'list', 'name': 'choix', 'message': 'Confirmez-vous votre décision ?', 'choices': ['Oui', 'Non']}]

    def display_info(self):
        print(self.__fiche)

    def make_choice(self):
        answers = prompt(self.__questions)
        if str.lower(answers['choix'][0]) in ['c', 'i']:
            answers2 = prompt(self.__questions2)
            if str.lower(answers2['choix']) == 'oui':
                if str.lower(answers['choix'][0]) == 'c':
                    res = ControleRepriseService().validation_fiche(self.__fiche, True)
                else:
                    res = ControleRepriseService().validation_fiche(self.__fiche, True)
                return res, self.__caller
            elif str.lower(answers2['choix']) == 'non':
                res = False
                return res, self.__caller
        elif str.lower(answers['choix'][0]) == 'a':
            return False, self.__caller
        else:
            raise ValueError
