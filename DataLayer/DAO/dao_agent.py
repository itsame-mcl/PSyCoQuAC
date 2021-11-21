from typing import List
import BusinessLayer.BusinessObjects.agent_factory as agent_factory
import DataLayer.DAO.interface_factory as interface_factory
from BusinessLayer.BusinessObjects.agent import Agent
from utils.singleton import Singleton
from hashlib import sha512


class DAOAgent(metaclass=Singleton):
    def __init__(self):
        self.__interface = interface_factory.InterfaceFactory.get_interface("Agent")

    @staticmethod
    def __saler_hasher_mdp(nom_utilisateur: str, mot_de_passe_en_clair: str) -> str:
        pwd = sha512()
        pwd.update(nom_utilisateur.encode("utf-8"))
        pwd.update(mot_de_passe_en_clair.encode("utf-8"))
        return pwd.hexdigest()

    def recuperer_agent(self, id_agent: int) -> Agent:
        data = self.__interface.recuperer_agent(id_agent)
        return agent_factory.AgentFactory.from_dict(data)

    def recuperer_equipe(self, id_superviseur: int) -> List[Agent]:
        data = self.__interface.recuperer_liste_agents(id_superviseur)
        equipe = list()
        for row in data:
            equipe.append(agent_factory.AgentFactory.from_dict(row))
        return equipe

    def deleguer_agent(self, id_agent: List[int], id_delegue: int) -> bool:
        return self.__interface.modifier_superviseur(list(id_agent), id_delegue)

    def deleguer_equipe(self, id_superviseur: int, id_delegue: int) -> bool:
        data = self.__interface.recuperer_liste_agents(id_superviseur)
        equipe = list()
        for row in data:
            equipe.append(row["identifiant_agent"])
        return self.__interface.modifier_superviseur(equipe, id_delegue)

    def creer_agent(self, infos_agent: Agent, nom_utilisateur: str, mot_de_passe: str) -> bool:
        data = infos_agent.as_dict()
        data["nom_utilisateur"] = nom_utilisateur
        data["mot_de_passe"] = self.__saler_hasher_mdp(nom_utilisateur, mot_de_passe)
        if data["est_superviseur"]:
            data["identifiant_superviseur"] = 0
        return self.__interface.creer_agent(data)

    def modifier_agent(self, agent_a_modifier: Agent) -> bool:
        return self.__interface.modifier_agent(agent_a_modifier.as_dict())

    def supprimer_agent(self, id_agent: int) -> bool:
        return self.__interface.supprimer_agent(id_agent)

    def promouvoir_agent(self, agent_a_promouvoir: int) -> bool:
        return self.__interface.promouvoir_agent(agent_a_promouvoir)

    def connexion_agent(self, nom_utilisateur: str, mot_de_passe: str) -> Agent:
        mot_de_passe_sale_hashe = self.__saler_hasher_mdp(nom_utilisateur, mot_de_passe)
        data = self.__interface.connexion_agent(nom_utilisateur, mot_de_passe_sale_hashe)
        if data is not None:
            agent = agent_factory.AgentFactory.from_dict(data)
            return agent
        else:
            raise ConnectionRefusedError

    def modifier_identifiants(self, id_agent: int, nom_utilisateur: str, mot_de_passe_en_clair: str) -> bool:
        mdp_sale_hashe = self.__saler_hasher_mdp(nom_utilisateur, mot_de_passe_en_clair)
        res = self.__interface.modifier_identifiants(id_agent, nom_utilisateur, mdp_sale_hashe)
        return res

    def verifier_identifiants(self, id_agent: int, nom_utilisateur: str, mot_de_passe_en_clair: str) -> bool:
        mdp_sale_hashe = self.__saler_hasher_mdp(nom_utilisateur, mot_de_passe_en_clair)
        res = self.__interface.verifier_identifiants(id_agent, nom_utilisateur, mdp_sale_hashe)
        return res

    def recuperer_nom_utilisateur(self, id_agent: int) -> str:
        return self.__interface.recuperer_nom_utilisateur(id_agent)

    def recuperer_dernier_id_agent(self) -> int:
        return self.__interface.recuperer_dernier_id_agent()

    def recuperer_id_superviseur(self, id_agent: int) -> int:
        return self.__interface.recuperer_id_superviseur(id_agent)
