from pprint import pprint
from PyInquirer import  prompt
from ViewLayer.CLI.abstract_view import AbstractView
from DataLayer import DAO as dao
from BusinessLayer.BusinessObjects.agent_factory import AgentFactory as factory

class NouvelUtilisateur(AbstractView):

    def __init__(self) -> None:

        self.__questions = [{'type': 'input','name': 'prenom','message': 'Prénom :'}, {'type': 'input','name': 'nom','message': 'NOM :',},
            {'type': 'input','name': 'est_superviseur','message': 'Rôle :'}, {'type': 'input','name': 'quotite','message': 'Quotité de travail :'},
            {'type': 'input','name': 'nom_utilisateur','message': "Nom d'utilisateur :"}, {'type': 'input','name': 'est_superviseur','message': 'Rôle :'},
            {'type': 'password','name': 'mot_de_passe','message': 'Mot de passe'}]
        self.__questions2 = [{'type': 'input', 'name': 'identifiant_superviseur', 'message': 'Identifiant du superviseur :'}]

    def enregistrement(self):
        answers = prompt(self.__questions)
        if str.lower(answers["est_superviseur"]) == "gestionnaire":
            answers2 = prompt(self.__questions2)
            answers.update(answers2)
        id_agent  = dao.DAOAgent.recuperer_prochain_id
        nouvel_agent = factory.from_dict(answers)
        probleme = dao.DAOAgent.creer_agent(nouvel_agent, answers['nom_utilisateur'], answers['mot_de_passe'])
        if not(probleme):
            print("L'enregistrement a échoué. Veuillez réessayer.")
            return NouvelUtilisateur.enregistrement
        else:
            from ViewLayer.CLI.menu import MenuView
            return MenuView()