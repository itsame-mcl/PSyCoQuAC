from PyInquirer import prompt
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.session import Session

class MenuPrincipalView(AbstractView):

    def __init__(self, session : Session) -> None:
        self.__questions = [{'type': 'list','name': 'choix','message': 'Bonjour '+session.agent.prenom+', que voulez-vous faire ?',
                            'choices': ['A) Consulter son pot', 'B) Modifier son compte','C) Se déconnecter']}]
        self.__questions2 = [{'type': 'list','name': 'choix 2','message': 'Bonjour '+session.agent.prenom+', que voulez-vous faire ?',
                            'choices': ['A) Consulter son pot', 'B) Modifier son compte','C) Se déconnecter'
                            'D) Déleguer son équipe', 'E) Déléguer un agent','F) Modifier un agent',
                            "G) Changer les droits d'un agent", 'H) Créer un nouvel utilisateur', "I) Gestion de l'équipe"
                            "J) Importer/Exporter des fichiers d'adresse"]}]

    def make_choice(self, session : Session):
        if session.agent.agent_id == 0:
            from ViewLayer.CLI.start_view import StartView
            return StartView()
        else:
            if session.droits:
                answers = prompt(self.__questions2)
            else:
                answers = prompt(self.__questions)
            if 'A' in str.upper(answers['choix']):
                from ViewLayer.CLI.consulter_pot_agent import ConsulterPotView
                return ConsulterPotView(session)
            elif 'B' in str.upper(answers['choix']) or 'F' in str.upper(answers['choix']):
                from ViewLayer.CLI.modifier_view import ModifierView
                return ModifierView(session)
            elif 'C' in str.upper(answers['choix']):
                from ViewLayer.CLI.deconnexion_view import DeconnexionView
                return DeconnexionView(session)
            elif 'D' in str.upper(answers['choix']) or 'E' in str.upper(answers['choix']):
                from ViewLayer.CLI.deleguer_view import DeleguerView
                return DeleguerView(session)
            elif 'G' in str.upper(answers['choix']):
                from ViewLayer.CLI.changer_droits_view import ChangerDroitsView
                return ChangerDroitsView(session)
            elif 'H' in str.upper(answers['choix']):
                from ViewLayer.CLI.nouvel_utilisateur_view import NouvelUtilisateurView
                return NouvelUtilisateurView(session)
            elif 'I' in str.upper(answers['choix']):
                from ViewLayer.CLI.gestion_equipe_view import GestionEquipeView
                return GestionEquipeView(session)
            elif 'J' in str.upper(answers['choix']):
                from ViewLayer.CLI.import_export_view import ImportExportView
                return ImportExportView(session)