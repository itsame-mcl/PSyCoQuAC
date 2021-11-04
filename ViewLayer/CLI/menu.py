from PyInquirer import prompt
from ViewLayer.CLI.session import Session

class MenuPrincipalView:

    def __init__(self, session : Session) -> None:
        self.__questions = [{'type': 'list','name': 'choix','message': 'Bonjour '+str(Session().prenom),
                            'choices': ['1) Consulter son pot', '2) Modifier son compte','3) Se déconnecter']}]
        self.__questions2 = [{'type': 'list','name': 'choix 2','message': 'Que voulez-vous faire ?',
                            'choices': ['4) Déleguer son équipe', '5) Déléguer un agent','6) Modifier un agent',
                            "7) Changer les droits d'un agent", '8) Créer un nouvel utilisateur']}]

    def naviguer(self, session : Session):
        if session.agent.agent_id == 0:
            from ViewLayer.CLI.connexion_view import ConnexionView
            return ConnexionView.connexion()
        else:
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
                from ViewLayer.CLI.modifier_compte_view import ModifierCompteView
                return ModifierCompteView.modifier(session)
            elif '3' in answers['choix']:
                from ViewLayer.CLI.deconnexion_view import DeconnexionView
                return DeconnexionView.deconnexion(session)
            elif '4' in answers['choix'] or '5' in answers['choix']:
                from ViewLayer.CLI.deleguer_view import DeleguerView
                return DeleguerView.deleguer(session)
            elif '6' in answers['choix'] :
                from ViewLayer.CLI.modifier_agent_view import ModifierAgentView
                return ModifierAgentView.modifier(session)
            elif '7' in answers['choix']:
                from ViewLayer.CLI.changer_droits_view import ChangerDroitsView
                return ChangerDroitsView.modifier(session)
            elif '8' in answers['choix']:
                from ViewLayer.CLI.nouvel_utilisateur_view import NouvelUtilisateurView
                return NouvelUtilisateurView.enregistrement(session)