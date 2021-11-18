from BusinessLayer.BusinessObjects.agent import Agent
import BusinessLayer.BusinessObjects.agent_factory as agent_factory
from DataLayer.DAO.dao_agent import DAOAgent
from utils.singleton import Singleton
from typing import List


class AgentService(metaclass=Singleton):
    @staticmethod
    def creer_agent(est_superviseur: bool, quotite: float, id_superviseur: int, nom_utilisateur: str,
                    mot_de_passe: str, prenom: str, nom: str) -> bool:
        data_agent = {'est_superviseur': est_superviseur, 'prenom': prenom, 'nom': nom, 'quotite': quotite,
                      'id_superviseur': id_superviseur, 'identifiant_agent': None}
        nouvel_agent = agent_factory.AgentFactory.from_dict(data_agent)
        return DAOAgent().creer_agent(nouvel_agent, nom_utilisateur, mot_de_passe)

    @staticmethod
    def modifier_agent(agent_a_modifier: dict) -> bool:
        return DAOAgent().modifier_agent(agent_a_modifier)

    @staticmethod
    def changer_droits(id_agent: int) -> bool:
        agent_a_modifier = DAOAgent().recuperer_agent(id_agent)
        return DAOAgent().changer_droits(agent_a_modifier)

    @staticmethod
    def supprimer_agent(agent_a_supprimer: int) -> bool:
        return DAOAgent().supprimer_agent(agent_a_supprimer)

    @staticmethod
    def recuperer_id_superviseur(id_agent: int) -> int:
        return DAOAgent().recuperer_id_superviseur(id_agent)['id_superviseur']

    @staticmethod
    def recuperer_equipe(id_superviseur: int) -> List[Agent]:
        return DAOAgent().recuperer_equipe(id_superviseur)

    @staticmethod
    def ajout_agent_equipe(id_superviseur: int, id_agent: int) -> bool:
        agent_a_modifier = DAOAgent().recuperer_agent(id_agent)
        agent_a_modifier.superviseur_id = id_superviseur
        return DAOAgent().modifier_agent(agent_a_modifier.as_dict())

    @staticmethod
    def promouvoir_agent(id_agent: int) -> bool:
        agent = DAOAgent().recuperer_agent(id_agent)
        return DAOAgent().changer_droits(agent)

    @staticmethod
    def deleguer_agent(id_agent: int, id_delegue: int) -> bool:
        return DAOAgent().deleguer_agent(id_agent, id_delegue)

    @staticmethod
    def deleguer_equipe(id_superviseur: int, id_delegue: int) -> bool:
        return DAOAgent().deleguer_equipe(id_superviseur, id_delegue)
