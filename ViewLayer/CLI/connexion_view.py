from PyInquirer import  prompt
from DataLayer import DAO as dao
from ViewLayer.CLI.session import Session
from BusinessLayer.BusinessObjects.agent import Agent

class ConnexionView:
    
    def __init__(self) -> None:
        self.__questions = [{'type': 'input','name': 'nom_utilisateur','message': "Nom d'utilisateur"}, 
                            {'type': 'input','name': 'mot_de_passe','message': 'Mot de passe :'}]

    def connexion(self):
        answers = prompt(self.__questions)
        agent = dao.DAOAgent.connexion_agent(answers['nom_utilisateur'], answers['mot_de_passe'])
        if not(isinstance(agent, Agent)):
            print("Ah ah ah... Vous n'avez pas dis le mot magique !. Veuillez réessayer.")
            return ConnexionView.connexion()
        else:
            session = Session(agent)
            from ViewLayer.CLI.menu import MenuPrincipalView
            return MenuPrincipalView(session)