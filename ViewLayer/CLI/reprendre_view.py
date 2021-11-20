from BusinessLayer.BusinessObjects.adresse import Adresse
from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.session import Session
from BusinessLayer.WebServices.BANClient import BANClient
from BusinessLayer.LocalServices.TraitementFA.controle_reprise_service import ControleRepriseService
from PyInquirer import prompt
import ViewLayer.CLI.menu as mp


class ReprendreView(AbstractView):
    def __init__(self, curseur: int = 0) -> None:
        self.__curseur = curseur
        self.__questions = [{'type': 'list', 'name': 'choix', 'message': 'Que voulez-vous faire ?',
                             'choices': ["a) Modifier l'adresse", 'c) Modifier les coordonnées GPS',
                                         'v) Valider la fiche', 'd) Marquer la fiche en déchet',
                                         'p) Passer à la fiche précédente', 's) Passer à la fiche suivante',
                                         'm) Retourner au menu principal']}]
        self.__questions2 = [
            {'type': 'list', 'name': 'choix', 'message': 'Confirmez-vous ?', 'choices': ['Oui', 'Non']}]
        self.__questions3 = [{'type': 'input', 'name': 'numero', 'message': 'Numéro de voie :'},
                             {'type': 'input', 'name': 'voie', 'message': 'Nom de la voie', },
                             {'type': 'input', 'name': 'cp', 'message': 'Code postal :'},
                             {'type': 'input', 'name': 'ville', 'message': 'Ville :'}]
        self.__questions4 = [{'type': 'list', 'name': 'choix', 'message': "Voulez vous resoumettre la fiche à l'API ?",
                              'choices': ['Oui', 'Non']}]
        self.__questions5 = [{'type': 'input', 'name': 'lat', 'message': 'Latitude :'},
                             {'type': 'input', 'name': 'lon', 'message': 'Longitude :'}]

    def display_info(self):
        pot = ControleRepriseService().consulter_pot(Session().agent.agent_id)
        if len(pot) > 0:
            fiche = pot[self.__curseur]
            print('Fiche adresse n°' + str(fiche.fiche_id) + 'Données initiales : adresse initiale : ' + 
                str(fiche.adresse_initiale) + 'Données API : Adresse finale : ' + str(fiche.adresse_finale) + 
                'Coordonnées GPS :' + str(fiche.coords_wgs84))
        else:
            print("Le pot est vide.")

    def __choix_modifier_adresse(self, fiche: FicheAdresse):
        answers3 = prompt(self.__questions3)
        nouvelle_adresse = Adresse(answers3['numero'], answers3['voie'], answers3['cp'], answers3['ville'])
        fiche.adresse_finale = nouvelle_adresse
        res = ControleRepriseService().modifier_fiche(fiche)
        return res

    def __choix_modifier_coordonnees(self, fiche: FicheAdresse):
        answers5 = prompt(self.__questions5)
        nouvelles_coords = (answers5['lat'], answers5['lon'])
        fiche.coords_wgs84 = nouvelles_coords
        res = ControleRepriseService().modifier_fiche(fiche)
        return res

    def __soumettre_api(self, fiche: FicheAdresse, reverse: bool = False):
        answers4 = prompt(self.__questions4)
        if str.lower(answers4['choix']) == 'oui':
            # Resoumettre à l'API
            if not reverse:
                score, fiche = BANClient().geocodage_par_fiche(fiche)
            else:
                score, fiche = BANClient().reverse_par_fiche(fiche)
            print("Le score de l'API est " + str(score))
            res = ControleRepriseService().modifier_fiche(fiche)
            return res
        else:
            return True

    def __confirmation(self):
        answers2 = prompt(self.__questions2)
        if str.lower(answers2['choix']) == 'oui':
            return True
        elif str.lower(answers2['choix']) == 'non':
            return False
        else:
            raise ValueError

    def make_choice(self):
        pot = ControleRepriseService().consulter_pot(Session().agent.agent_id)
        if len(pot) > 0:
            fiche = pot[self.__curseur]
            answers = prompt(self.__questions)
            if str.lower(answers['choix'][0]) == 'a':
                res = self.__choix_modifier_adresse(fiche)
                if res:
                    res2 = self.__soumettre_api(fiche)
                    if not res2:
                        print("Échec dans l'enregistrement des modifications.")
                else:
                    print("Échec dans l'enregistrement des modifications.")
                return ReprendreView(self.__curseur)
            elif str.lower(answers['choix'][0]) == 'c':
                res = self.__choix_modifier_coordonnees(fiche)
                if res:
                    res2 = self.__soumettre_api(fiche, True)
                    if not res2:
                        print("Échec dans l'enregistrement des modifications.")
                else:
                    print("Échec dans l'enregistrement des modifications.")
                return ReprendreView(self.__curseur)
            elif str.lower(answers['choix'][0]) in ['v', 'd']:
                ans = self.__confirmation()
                if ans:
                    if str.lower(answers['choix'][0]) == 'v':
                        fiche.code_res = "VR"
                    else:
                        fiche.code_res = "DR"
                    res = ControleRepriseService.modifier_fiche(fiche)
                    if res:
                        if len(pot) > 1:
                            return ReprendreView(self.__curseur % (len(pot) - 1))
                        else:
                            return ReprendreView(0)
                    else:
                        print("Échec dans l'enregistrement des modifications.")
                        return ReprendreView(self.__curseur)
                else:
                    return ReprendreView(self.__curseur)
            elif str.lower(answers['choix'][0]) == 'p':
                curseur = (self.__curseur - 1) % len(pot)
                return ReprendreView(curseur)
            elif str.lower(answers['choix'][0]) == 's':
                curseur = (self.__curseur + 1) % len(pot)
                return ReprendreView(curseur)
            elif str.lower(answers['choix'][0]) == 'm':
                return mp.MenuPrincipalView()
            else:
                return ReprendreView(self.__curseur)
        else:
            return mp.MenuPrincipalView()
