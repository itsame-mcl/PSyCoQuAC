from PyInquirer import prompt
from BusinessLayer.LocalServices.Gestion.agent_service import AgentService
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.menu import MenuPrincipalView
from ViewLayer.CLI.session import Session

class ModifierView(AbstractView):

    def __init__(self) -> None:
        self.__questions0 = [{'type': 'list','name': 'choix','message': 'Quelle(s) information(s) souhaitez-vous modifier ?',
                            'choices': ['1) Prénom', '2) Nom','3) Quotité de travail',"4) Nom d'utilisateur",'5) Mot de passe', '6) Retourner au menu principal']}]
        self.__questions1 = [{'type': 'input','name': 'prenom','message': "Quel est votre nouveau prénom ?"}]
        self.__questions2 = [{'type': 'input','name': 'nom','message': "Quel est votre nouveau nom ?"}]
        self.__questions3 = [{'type': 'input','name': 'quotite','message': "Quelle est votre nouvelle quotité de travail ?"}]
        self.__questions4 = [{'type': 'input','name': 'util','message': "Quel est votre nouveau nom d'utilisateur ?"},
                            {'type': 'input','name': 'mdp','message': "Quel est votre mot-de-passe ?"}]
        self.__questions5 = [{'type': 'input','name': 'mdp','message': "Quel est votre nouveau mot-de-passe ?"},
                            {'type': 'input','name': 'util','message': "Quel est votre nom d'utilisateur ?"}]
        self.__questions = [{'type': 'list','name': 'choix','message': 'Souhaitez-vous modifier autre chose ?',
                            'choices': ['O) Oui', 'N) Non']}]

    def display_info(self, session : Session):
        print('   Agent n°:' + str(session.utilisateur_connecte.agent_id) + '\nPrénom : ' + str(session.utilisateur_connecte.prenom) + '\nNom : '  + str(session.utilisateur_connecte.nom) + '\nQuotité de travail : ' + str(session.utilisateur_connecte.quotite))
    
    def make_choice(self):
        answers0 = prompt(self.__questions0)
        if '1' in answers0['choix']:
            answers1 = prompt(self.__questions1)
            Session().agent.prenom = answers1['prenom']
            probleme = AgentService.modifier_agent(Session().agent.as_dict())
            if not(probleme):
                print('La modification a échoué. Veuillez réessayer ultérieurement.')
            answers = prompt(self.__questions)
            if 'o' in str.lower(answers['choix']):
                return ModifierView()
            else:
                return MenuPrincipalView()
        elif '2' in answers0['choix']:
            answers2 = prompt(self.__questions2)
            Session().agent.nom = answers2['nom']
            probleme = AgentService.modifier_agent(Session().agent.as_dict())
            if not(probleme):
                print('La modification a échoué. Veuillez réessayer ultérieurement.')
            answers = prompt(self.__questions)
            if 'o' in str.lower(answers['choix']):
                return ModifierView()
            else:
                return MenuPrincipalView()
        elif '3' in answers0['choix']:
            answers3 = prompt(self.__questions3)
            Session().agent.quotite = answers3['quotite']
            probleme = AgentService.modifier_agent(Session().agent.as_dict())
            if not(probleme):
                print('La modification a échoué. Veuillez réessayer ultérieurement.')
            answers = prompt(self.__questions)
            if 'o' in str.lower(answers['choix']):
                return ModifierView()
            else:
                return MenuPrincipalView()
        elif '4' in answers0['choix']:
            answers4 = prompt(self.__questions4)
            nouveau_mdp_hache = AgentService.saler_hasher_mdp(answers4['util'], answers4['mdp'])
            nouvel_agent = {'nom_utilisateur' : answers4['util'], 'mot_de_passe' : nouveau_mdp_hache}
            probleme = AgentService.modifier_agent(nouvel_agent)
            if not(probleme):
                print("La modification a échoué. Veuillez réessayer ultérieurement.")
            answers = prompt(self.__questions)
            if 'o' in str.lower(answers['choix']):
                return ModifierView()
            else:
                return MenuPrincipalView()
        elif '5' in answers0['choix']:
            answers5 = prompt(self.__questions5)
            nouveau_mdp_hache = AgentService.saler_hasher_mdp(answers5['util'], answers5['mdp'])
            nouvel_agent = {'mot_de_passe' : nouveau_mdp_hache}
            probleme = AgentService.modifier_agent(nouvel_agent)
            if not(probleme):
                print("La modification a échoué. Veuillez réessayer ultérieurement.")
            answers = prompt(self.__questions)
            if 'o' in str.lower(answers['choix']):
                return ModifierView()
            else:
                return MenuPrincipalView()
        else:
            return MenuPrincipalView()