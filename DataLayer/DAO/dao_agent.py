from typing import List

import BusinessLayer.BusinessObjects.agent_factory as agent_factory
import DataLayer.DAO.interface_factory as interface_factory
from BusinessLayer.BusinessObjects.agent import Agent
from utils.singleton import Singleton
from hashlib import sha512


class DAOAgent(metaclass=Singleton):

    def __init__(self):
        self.__interface = interface_factory.InterfaceFactory.get_interface("Agent")

    def __saler_hasher_mdp(self, nom_utilisateur: str, mot_de_passe_en_clair: str) -> str:
        pwd = sha512()
        pwd.update(nom_utilisateur.encode("utf-8"))
        pwd.update(mot_de_passe_en_clair.encode("utf-8"))
        mot_de_passe_sale_hashe = pwd.hexdigest()
        return mot_de_passe_sale_hashe

    def recuperer_agent(self, id_agent: int) -> Agent:
        data = self.__interface.recuperer_agent(id_agent)
        agent = agent_factory.AgentFactory.from_dict(data)
        return agent

    def recuperer_equipe(self, id_superviseur: int) -> List[Agent]:
        res = self.__interface.recuperer_liste_agents(id_superviseur)
        return res

    def deleguer_agent_a(self, id_agents: List[int], id_superviseur: int) -> bool:
        res = self.__interface.deleguer_agent_a(id_agents, id_superviseur)
        return res

    def creer_agent(self, infos_agent: Agent, nom_utilisateur: str, mot_de_passe: str) -> bool:
        data = infos_agent.as_dict()
        data["nom_utilisateur"] = nom_utilisateur
        data["mot_de_passe"] = self.__saler_hasher_mdp(nom_utilisateur, mot_de_passe)
        if data["est_superviseur"]:
            data["identifiant_superviseur"] = 0
        res = self.__interface.creer_agent(data)
        return res

    def modifier_agent(self, agent_a_modifier: Agent) -> bool:
        res = self.__interface.modifier_agent(agent_a_modifier.as_dict())
        return res

    def supprimer_agent(self, id_agent: int) -> bool:
        res = self.__interface.supprimer_agent(id_agent)
        return res

    def changer_droits(self, agent_a_modifier: Agent) -> bool:
        res = self.__interface.changer_droits(agent_a_modifier)
        return res
