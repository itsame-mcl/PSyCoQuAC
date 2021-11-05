from PyInquirer import prompt
from ViewLayer.CLI.session import Session
from BusinessLayer.LocalServices.Gestion.agent_service import AgentService
from ViewLayer.CLI.ModifierView.continuer_modif_view import ContinuerModifView

class ModifierUtilView:

    def __init__(self, session : Session) -> None:
        self.__questions = [{'type': 'input','name': 'util','message': "Quel est votre nouveau nom d'utilisateur ?"},
                            {'type': 'input','name': 'mdp','message': "Quel est votre mot-de-passe ?"}]

    def modifier_quotite(self, session: Session):
        answers = prompt(self.__questions)
        nouveau_mdp_hache = AgentService.saler_hasher_mdp(answers['util'], answers['mdp'])
        nouvel_agent = session.agent.as_dict()
        nouvel_agent['nom_utilisateur'] = answers['util']
        nouvel_agent['mot_de_passe'] = nouveau_mdp_hache
        nouvel_agent['est_superviseur'] = session.droits
        if nouvel_agent['est_superviseur']:
            nouvel_agent['id_superviseur'] = session.agent.agent_id
        else:
            nouvel_agent['id_superviseur'] = AgentService.recuperer_id_superviseur(session.agent.agent_id)
        probleme = AgentService.modifier_agent(nouvel_agent)
        if not(probleme):
            print("La modification a échoué. Veuillez réessayer ultérieurement.")
        return ContinuerModifView(session)