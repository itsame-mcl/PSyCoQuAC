from typing import Tuple
from typing import List

from BusinessLayer.BusinessObjects.agent import Agent
import DataLayer.DAO.interface_factory as Factory
from utils.singleton import Singleton

class DAOAgent(metaclass=Singleton):

    def __init__(self):
        self.__interface = Factory.InterfaceFactory.get_interface("Agent")

    def deleguer_agent_a(self, id_agents : List[int], id_superviseur : int) -> bool:
        res = self.__interface.deleguer_agent_a(id_agents, id_superviseur)
        return res

    def recuperer_liste_agents(self, id_superviseur : int) -> List[Agent]:
        res = self.__interface.recuperer_liste_agents(id_superviseur)
        return res

    def supprimer_agent(self, id_agent : int) -> bool:
        res = self.__interface.supprimer_agent(id_agent)
        return res

    def creer_agent(self, est_superviseur : bool, quotite : float, id_superviseur : int, nom_utilisateur : str, mot_de_passe : str, prenom : str, nom : str) -> bool:
        res = self.__interface.creer_agent( est_superviseur, quotite, id_superviseur, nom_utilisateur, mot_de_passe, prenom, nom)
        return res

    def modifier_agent(self, agent_a_modifier : Agent) -> bool:
        res = self.__interface.modifier_agent(agent_a_modifier)
        return res

    def changer_droits(self, agent_a_modifier : Agent) -> bool:
        res = self.__interface.changer_droits(agent_a_modifier)
        return res

    def recuperer_mdp_agent(self, nom_utilisateur : str, mot_de_passe : str) -> str:
        res = self.__interface.recuperer_mdp_agent(nom_utilisateur, mot_de_passe)
        return res
    
    def recuperer_agent_id(self, nom_utilisateur : str, mot_de_passe : str) -> int:
        res = self.__interface.recuperer_agent_id(nom_utilisateur, mot_de_passe)
        return res

    def recuperer_agent_identite(self, nom_utilisateur : str, mot_de_passe : str) -> Tuple:
        res = self.__interface.recuperer_agent_identite(nom_utilisateur, mot_de_passe)
        return res

    def recuperer_superviseur_id(self, nom_utilisateur : str, mot_de_passe : str) -> int:
        res = self.__interface.recuperer_superviseur_id(nom_utilisateur, mot_de_passe)
        return res