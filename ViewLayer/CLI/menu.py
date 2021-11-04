from PyInquirer import prompt
from ViewLayer.CLI.session import Session

class MenuPrincipalView:

    def __init__(self, session : Session) -> None:
        self.__questions = [{'type': 'list','name': 'choix','message': 'Bonjour '+str(Session().prenom),
                            'choices': ['1) Consulter son pot','2) Se déconnecter']}]
        self.__questions2 = [{'type': 'list','name': 'choix 2','message': 'Que voulez-vous faire ?',
                            'choices': ['3) Déleguer son équipe', '4) Déléguer un agent','5) Modifier un agent',
                            "6) Changer les droits d'un agent", '7) Créer un nouvel utilisateur']}]

    def naviguer(self, session : Session):
        with open('outils graphiques/bannière.txt', 'r', encoding = "utf-8") as asset:
            print(asset.read())
        answers = prompt(self.__questions)
        if session.droits:
            answers2 = prompt(self.__questions2)
            answers.update(answers2)
        if '1' in answers['choix']:
            from ViewLayer.CLI.consulter_pot import ConsulterPotView
            return ConsulterPotView(session)
        elif '2' in answers['choix']:
            from ViewLayer.CLI.deconnexion_view import DeconnexionView
            return DeconnexionView.deconnexion(session)
        elif '3' in answers['choix'] or '4' in answers['choix']:
            from ViewLayer.CLI.deleguer_view import DeleguerView
            return DeleguerView.deleguer(session)
        elif '5' in answers['choix'] :
            from ViewLayer.CLI.deconnexion_view import ModifierView
            return ModifierView.modifier(session)
        elif '6' in answers['choix']:
            from ViewLayer.CLI.changer_droits_view import ChangerDroitsView
            return ModifierView.modifier(session)
        elif '7' in answers['choix']:
            from ViewLayer.CLI.nouvel_utilisateur_view import NouvelUtilisateurView
            return NouvelUtilisateurView.enregistrement(session)