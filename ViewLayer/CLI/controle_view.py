from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.menu import MenuPrincipalView
from ViewLayer.CLI.session import Session
from BusinessLayer.LocalServices.TraitementFA.controle_reprise_service import ControleRepriseService
from PyInquirer import prompt


class ControlerView(AbstractView):
    def __init__(self, curseur: int = 0) -> None:
        self.__curseur = curseur
        self.__questions = [{'type': 'list', 'name': 'choix', 'message': 'Que voulez-vous faire ?',
                             'choices': ['c) Les données sont correctes', 'i) Les données sont incorrectes ',
                                         'p) Retourner à la fiche précédente', 's) Passer à la fiche suivante',
                                         'm) Retourner au menu principal']}]
        self.__questions2 = [
            {'type': 'list', 'name': 'choix', 'message': 'Confirmez-vous votre décision ?', 'choices': ['Oui', 'Non']}]

    def display_info(self):
        pot = ControleRepriseService().consulter_pot(Session().agent.agent_id)
        if len(pot) > 0:
            fiche = pot[self.__curseur]
            print('Fiche adresse n°' + str(fiche.fiche_id) + 'Données initiales : adresse initiale : ' +
                  str(fiche.adresse_initiale) + 'Données API : Adresse finale : ' + str(fiche.adresse_finale) +
                  'Coordonnées GPS :' + str(fiche.coords_wgs84))
        else:
            print("Le pot est vide.")

    def make_choice(self):
        pot = ControleRepriseService().consulter_pot(Session().agent.agent_id)
        if len(pot) > 0:
            fiche = pot[self.__curseur]
            answers = prompt(self.__questions)
            if str.lower(answers['choix'][0]) in ['c', 'i']:
                answers2 = prompt(self.__questions2)
                if str.lower(answers2['choix']) == 'oui':
                    if str.lower(answers['choix'][0]) == 'c':
                        res = ControleRepriseService().validation_fiche(fiche, True)
                    else:
                        res = ControleRepriseService().validation_fiche(fiche, True)
                elif str.lower(answers2['choix']) == 'non':
                    res = False
                else:
                    raise ValueError
                if res:
                    if len(pot) > 1:
                        return ControlerView(self.__curseur % (len(pot) - 1))
                    else:
                        return ControlerView(0)
                else:
                    return ControlerView(self.__curseur)
            elif str.lower(answers['choix'][0]) == 'p':
                curseur = (self.__curseur - 1) % len(pot)
                return ControlerView(curseur)
            elif str.lower(answers['choix'][0]) == 's':
                curseur = (self.__curseur + 1) % len(pot)
                return ControlerView(curseur)
            elif str.lower(answers['choix'][0]) == 'm':
                return MenuPrincipalView()
            else:
                return ControlerView(self.__curseur)
        else:
            return MenuPrincipalView()
