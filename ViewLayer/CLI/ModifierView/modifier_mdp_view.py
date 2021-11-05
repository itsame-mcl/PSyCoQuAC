from PyInquirer import prompt
from ViewLayer.CLI.session import Session
from BusinessLayer.LocalServices.Gestion.agent_service import AgentService
from ViewLayer.CLI.ModifierView.continuer_modif_view import ContinuerModifView

class ModifierMDPView:

    def __init__(self, session : Session) -> None:
        self.__questions = [{'type': 'input','name': 'mdp','message': "Quel est votre nouveau mot-de-passe ?"},
                            {'type': 'input','name': 'util','message': "Quel est votre nom d'utilisateur ?"}]

    def modifier_mdp(self, session: Session):
        answers = prompt(self.__questions)
        nouveau_mdp_hache = AgentService.saler_hasher_mdp(answers['util'], answers['mdp'])
        nouvel_agent = {'mot_de_passe' : nouveau_mdp_hache}
        probleme = AgentService.modifier_agent(nouvel_agent)
        if not(probleme):
            print("La modification a échoué. Veuillez réessayer ultérieurement.")
        return ContinuerModifView(session)