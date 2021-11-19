from PyInquirer import prompt
from BusinessLayer.LocalServices.Gestion.agent_service import AgentService
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.menu import MenuPrincipalView
from ViewLayer.CLI.session import Session
from BusinessLayer.BusinessObjects.agent import Agent


class ModifierView(AbstractView):
    def __init__(self, agent: Agent = None) -> None:
        if agent is None:
            self.__agent = Session().agent
        else:
            self.__agent = agent
        self.__questions0 = [{'type': 'list', 'name': 'choix', 'message': 'Quelle(s) information(s) souhaitez-vous modifier ?',
                            'choices': ['1) Prénom', '2) Nom', '3) Quotité de travail', "4) Nom d'utilisateur", '5) Mot de passe',
                            '6) Retourner au menu principal']}]
        self.__questions1 = [{'type': 'input', 'name': 'prenom', 'message': "Quel est le nouveau prénom ?"}]
        self.__questions2 = [{'type': 'input', 'name': 'nom', 'message': "Quel est le nouveau nom ?"}]
        self.__questions3 = [{'type': 'input', 'name': 'quotite', 'message': "Quelle est la nouvelle quotité de travail ?"}]
        self.__questions4 = [{'type': 'input', 'name': 'util', 'message': "Quel est le nouveau nom d'utilisateur ?"},
                             {'type': 'input', 'name': 'mdp', 'message': "Quel est le mot-de-passe ?"}]
        self.__questions5 = [{'type': 'input', 'name': 'mdp', 'message': "Quel est le nouveau mot-de-passe ?"},
                             {'type': 'input', 'name': 'util', 'message': "Quel est le nom d'utilisateur ?"}]
        self.__questions = [{'type': 'list', 'name': 'choix', 'message': 'Souhaitez-vous modifier autre chose ?',
                             'choices': ['O) Oui', 'N) Non']}]

    def display_info(self):
        print('   Agent n°:' + str(self.__agent.agent_id) + '\nPrénom : ' + str(self.__agent.prenom) + 
            '\nNom : ' + str(self.__agent.nom) + '\nQuotité de travail : ' + str(self.__agent.quotite))

    def make_choice(self):
        answers0 = prompt(self.__questions0)
        if '1' in answers0['choix']:
            answers1 = prompt(self.__questions1)
            self.__agent.prenom = answers1['prenom']
            succes = AgentService().modifier_agent(self.__agent.as_dict())
            if not(succes):
                print('La modification a échoué. Veuillez réessayer ultérieurement.')
            answers = prompt(self.__questions)
            if 'o' in str.lower(answers['choix']):
                return ModifierView()
            else:
                return MenuPrincipalView()
        elif '2' in answers0['choix']:
            answers2 = prompt(self.__questions2)
            self.__agent.nom = answers2['nom']
            succes = AgentService().modifier_agent(self.__agent.as_dict())
            if not(succes):
                print('La modification a échoué. Veuillez réessayer ultérieurement.')
            answers = prompt(self.__questions)
            if 'o' in str.lower(answers['choix']):
                return ModifierView()
            else:
                return MenuPrincipalView()
        elif '3' in answers0['choix']:
            answers3 = prompt(self.__questions3)
            self.__agent.quotite = answers3['quotite']
            succes = AgentService().modifier_agent(self.__agent.as_dict())
            if not(succes):
                print('La modification a échoué. Veuillez réessayer ultérieurement.')
            answers = prompt(self.__questions)
            if 'o' in str.lower(answers['choix']):
                return ModifierView()
            else:
                return MenuPrincipalView()
        elif '4' in answers0['choix']:
            answers4 = prompt(self.__questions4)
            nouveau_mdp_hache = AgentService().saler_hasher_mdp(answers4['util'], answers4['mdp'])
            nouvel_agent = {'nom_utilisateur': answers4['util'], 'mot_de_passe': nouveau_mdp_hache}
            succes = AgentService().modifier_agent(nouvel_agent)
            if not(succes):
                print("La modification a échoué. Veuillez réessayer ultérieurement.")
            answers = prompt(self.__questions)
            if 'o' in str.lower(answers['choix']):
                return ModifierView()
            else:
                return MenuPrincipalView()
        elif '5' in answers0['choix']:
            answers5 = prompt(self.__questions5)
            nouveau_mdp_hache = AgentService().saler_hasher_mdp(answers5['util'], answers5['mdp'])
            nouvel_agent = {'mot_de_passe': nouveau_mdp_hache}
            succes = AgentService().modifier_agent(nouvel_agent)
            if not(succes):
                print("La modification a échoué. Veuillez réessayer ultérieurement.")
            answers = prompt(self.__questions)
            if 'o' in str.lower(answers['choix']):
                return ModifierView()
            else:
                return MenuPrincipalView()
        else:
            return MenuPrincipalView()
