from BusinessLayer.BusinessObjects.adresse import Adresse
from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from ViewLayer.CLI.abstract_view import AbstractView
from BusinessLayer.WebServices.BANClient import BANClient
from BusinessLayer.LocalServices.TraitementFA.controle_reprise_service import ControleRepriseService
from PyInquirer import prompt
from copy import deepcopy


class ReprendreView(AbstractView):
    def __init__(self, caller: AbstractView, fiche: FicheAdresse) -> None:
        self.__caller = caller
        self.__fiche = fiche
        self.__questions = [{'type': 'list', 'name': 'choix', 'message': 'Que voulez-vous faire ?',
                             'choices': ["A) Modifier l'adresse", 'C) Modifier les coordonnées GPS',
                                         'V) Valider la fiche', 'D) Marquer la fiche en déchet',
                                         'Q) Décider plus tard']}]
        self.__oui_non = [
            {'type': 'list', 'name': 'choix', 'message': '', 'choices': ['Oui', 'Non']}]

    def __choix_modifier_adresse(self):
        prompt_adresse = [{'type': 'input', 'name': 'numero', 'message': 'Numéro de voie :',
                           'default': self.__fiche.adresse_finale.numero},
                             {'type': 'input', 'name': 'voie', 'message': 'Nom de la voie',
                              'default': self.__fiche.adresse_finale.voie},
                             {'type': 'input', 'name': 'cp', 'message': 'Code postal :',
                              'default': self.__fiche.adresse_finale.cp},
                             {'type': 'input', 'name': 'ville', 'message': 'Ville :',
                              'default': self.__fiche.adresse_finale.ville}]
        nouv_data = prompt(prompt_adresse)
        nouvelle_adresse = Adresse(nouv_data['numero'], nouv_data['voie'], nouv_data['cp'], nouv_data['ville'])
        self.__fiche.adresse_finale = nouvelle_adresse

    def __choix_modifier_wgs84(self):
        prompt_wgs84 = [{'type': 'input', 'name': 'lat', 'message': 'Latitude :',
                         'default': self.__fiche.coords_wgs84[1]},
                             {'type': 'input', 'name': 'lon', 'message': 'Longitude :',
                              'default': self.__fiche.coords_wgs84[0]}]
        nouvelles_coords = prompt(prompt_wgs84)
        self.__fiche.coords_wgs84 = (nouvelles_coords['lon'], nouvelles_coords['lat'])

    def __soumettre_api(self, reverse: bool = False):
        prompt_api = self.__oui_non
        prompt_api[0]["message"] = "Voulez vous resoumettre la fiche à l'API ?"
        answer = prompt(prompt_api)
        if str.upper(answer['choix'][0]) == 'O':
            original = deepcopy(self.__fiche)
            # Resoumettre à l'API
            if not reverse:
                score, prop_fiche = BANClient().geocodage_par_fiche(self.__fiche)
            else:
                score, prop_fiche = BANClient().reverse_par_fiche(self.__fiche)
            print("La fiche proposée par l'API est :")
            print(prop_fiche)
            print("Le score de confiance de l'API est " + str(score))
            prompt_conservation = [
                {'type': 'list', 'name': 'choix', 'message': "Quelle fiche souhaitez-vous conserver ?",
                 'choices': ["A) La fiche recodée par l'API", "M) La fiche saisie manuellement"]}]
            choix_conservation = prompt(prompt_conservation)
            if str.upper(choix_conservation['choix']) == 'A':
                self.__fiche = prop_fiche
            else:
                self.__fiche = original

    def __confirmation(self):
        prompt_conf = self.__oui_non
        prompt_conf[0]["message"] = "Voulez vous confirmer votre choix ?"
        answer = prompt(prompt_conf)
        if str.upper(answer['choix'][0]) == 'O':
            return True
        elif str.lower(answer['choix'][0]) == 'N':
            return False
        else:
            raise ValueError

    def make_choice(self):
        flag_continue = True
        res = False
        while flag_continue:
            print(self.__fiche)
            answers = prompt(self.__questions)
            if str.upper(answers['choix'][0]) == 'A':
                self.__choix_modifier_adresse()
                self.__soumettre_api()
            elif str.upper(answers['choix'][0]) == 'C':
                self.__choix_modifier_wgs84()
                self.__soumettre_api(reverse=True)
            elif str.upper(answers['choix'][0]) in ['V', 'D']:
                ans = self.__confirmation()
                if ans:
                    flag_continue = False
                    if str.upper(answers['choix'][0]) == 'V':
                        res = ControleRepriseService().validation_fiche(self.__fiche, True)
                    else:
                        res = ControleRepriseService().validation_fiche(self.__fiche, False)
            elif str.upper(answers['choix'][0]) == 'Q':
                flag_continue = False
                res = False
            else:
                raise ValueError
        return res, self.__fiche, self.__caller
