from PyInquirer import prompt
from ViewLayer.CLI.session import Session
from BusinessLayer.LocalServices.Gestion.fiche_agent_service import AgentServices
from ViewLayer.CLI.ModifierView.continuer_modif_view import ContinuerModifView

class ModifierUtilView:

    def __init__(self, session : Session) -> None:
        self.__questions = [{'type': 'input','name': 'util','message': "Quel est votre nouveau nom d'utilisateur ?"},
                            {'type': 'input','name': 'mdp','message': "Quel est votre mot-de-passe ?"}]

    def modifier_quotite(self, session: Session):
        answers = prompt(self.__questions)
        nouveau_mdp_hache = 
        nouvel_agent = 
        probleme = AgentServices.modifier_agent(nouvel_agent) # on récupère un booléen afin de savoir si l'opération a réussi ou échoué
        if not(probleme):
            print("La modification a échoué. Veuillez réessayer ultérieurement.")
        return ContinuerModifView(session)

# Il faut récupérer le mot de passe et le nom d'utilisateur (2 services qui font appel à 2 méthodes de la DAO).
# Il faut récupérer le mot de passe de l'agent, pour hacher/saler avec son nouveau nom d'utilisateur.