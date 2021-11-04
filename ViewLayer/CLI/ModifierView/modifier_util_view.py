from PyInquirer import prompt
from ViewLayer.CLI.session import Session
from DataLayer import DAO as dao
from ViewLayer.CLI.ModifierView.continuer_modif_view import ContinuerModifView

class ModifierUtilView:

    def __init__(self) -> None:
        self.__questions = [{'type': 'input','name': 'util','message': "Quel est votre nouveau nom d'utilisateur ?"},
                            {'type': 'input','name': 'mdp','message': "Quel est votre mot-de-passe ?"}]

    def modifier_quotite(self, session: Session):
        answers = prompt(self.__questions)
        nouveau_mdp_hache = 
        nouvel_agent = 
        dao.DAOAgent.modifier_agent(nouvel_agent)
        return ContinuerModifView.continuer(session)

# Il faut récupérer le mot de passe et le nom d'utilisateur (2 services qui font appel à 2 méthodes de la DAO).
# Il faut récupérer le mot de passe de l'agent, pour hacher/saler avec son nouveau nom d'utilisateur.