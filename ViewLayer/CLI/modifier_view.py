from PyInquirer import prompt

from BusinessLayer.BusinessObjects.gestionnaire import Gestionnaire
from BusinessLayer.LocalServices.Gestion.agent_service import AgentService
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.session import Session
from BusinessLayer.BusinessObjects.agent import Agent
import ViewLayer.CLI.menu as mp


class ModifierView(AbstractView):
    def __init__(self, agent: Agent = None) -> None:
        if agent is None:
            self.__agent = Session().agent
            self.__modal = False
        else:
            self.__agent = agent
            self.__modal = True
        self.__main_prompt = [{'type': 'list', 'name': 'choix',
                               'message': 'Quelle information souhaitez-vous modifier ?',
                               'choices': ['P) Prénom', 'N) Nom']}]
        if Session().droits:
            self.__main_prompt[0]['choices'].append("T) Quotité de travail")
        if not self.__modal:
            self.__main_prompt[0]['choices'].append("I) Identifiants (nom d'utilisateur/mot de passe)")
        if Session().droits and self.__modal:
            self.__main_prompt[0]['choices'].append(
                "R) Réinitialiser les identifiants (nom d'utilisateur/mot de passe)")
        if Session().droits and self.__modal and isinstance(self.__agent, Gestionnaire):
            self.__main_prompt[0]['choices'].append("V) Promouvoir le gestionnaire en superviseur")
        self.__main_prompt[0]['choices'].append('Q) Retourner au menu principal')
        self.__continue_prompt = [{'type': 'list', 'name': 'choix', 'message': 'Souhaitez-vous modifier autre chose ?',
                                   'choices': ['O) Oui', 'N) Non']}]

    def display_info(self):
        print('   Agent n°:' + str(self.__agent.agent_id) + '\nPrénom : ' + str(self.__agent.prenom) +
              '\nNom : ' + str(self.__agent.nom) + '\nQuotité de travail : ' + str(self.__agent.quotite))

    def make_choice(self):
        continuer = True
        while continuer:
            answers0 = prompt(self.__main_prompt)
            if str.upper(answers0['choix'][0]) == "Q":
                continuer = False
            else:
                if str.upper(answers0['choix'][0]) == "P":
                    prompt_prenom = [{'type': 'input', 'name': 'prenom', 'message': "Quel est le nouveau prénom ?"}]
                    answer = prompt(prompt_prenom)
                    self.__agent.prenom = answer['prenom']
                    succes = AgentService().modifier_agent(self.__agent)
                elif str.upper(answers0['choix'][0]) == "N":
                    prompt_nom = [{'type': 'input', 'name': 'nom', 'message': "Quel est le nouveau nom ?"}]
                    answer = prompt(prompt_nom)
                    self.__agent.nom = answer['nom']
                    succes = AgentService().modifier_agent(self.__agent)
                elif str.upper(answers0['choix'][0]) == "T":
                    prompt_quotite = [{'type': 'input', 'name': 'quotite',
                                       'message': "Quelle est la nouvelle quotité de travail ?"}]
                    answers = prompt(prompt_quotite)
                    self.__agent.quotite = answers['quotite']
                    succes = AgentService().modifier_agent(self.__agent)
                elif str.upper(answers0['choix'][0]) == "I":
                    prompt_chgmt = [{'type': 'input', 'name': 'login', 'message': "Quel est votre nom d'utilisateur ?"},
                                    {'type': 'input', 'name': 'mdp', 'message': "Quel est votre mot de passe ?"},
                                    {'type': 'input', 'name': 'n_login',
                                     'message': "Quel est votre nouveau nom d'utilisateur "
                                                "(laisser vide pour ne pas modifier) ?"},
                                    {'type': 'input', 'name': 'n_mdp',
                                     'message': "Quel est votre nouveau mot de passe "
                                                "(laisser vide pour ne pas modifier) ?"}]
                    answer = prompt(prompt_chgmt)
                    if answer['n_login'] == '':
                        answer['n_login'] = None
                    if answer['n_mdp'] == '':
                        answer['n_mdp'] = None
                    succes = AgentService().changer_identifiants(self.__agent.agent_id, answer['login'], answer['mdp'],
                                                                 answer['n_login'], answer['n_mdp'])
                elif str.upper(answers0['choix'][0]) == "R":
                    prompt_reinit = [{'type': 'input', 'name': 'n_login',
                                      'message': "Quel est le nouveau nom d'utilisateur "
                                                 "(laisser vide pour ne pas modifier) ?"},
                                     {'type': 'input', 'name': 'n_mdp',
                                      'message': "Quel est le nouveau mot de passe (obligatoire) ?"}]
                    answer = prompt(prompt_reinit)
                    if answer['n_login'] == '':
                        answer['n_login'] = None
                    succes = AgentService().reinitialiser_identifiants(self.__agent.agent_id, answer['n_mdp'],
                                                                       answer['n_login'])
                elif str.upper(answers0['choix'][0]) == "V":
                    succes = AgentService().promouvoir_agent(self.__agent.agent_id)
                else:
                    succes = True  # Clause ramasse-miette pour éviter un message d'erreur intempestif
                if not succes:
                    print('La modification a échoué. Veuillez réessayer ultérieurement.')
                answer_continuer = prompt(self.__continue_prompt)
                if str.upper(answer_continuer['choix'][0]) == "O":
                    continuer = True
                else:
                    continuer = False
        if self.__modal:
            return 0
        else:
            return mp.MenuPrincipalView()
