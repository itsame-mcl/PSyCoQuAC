from BusinessLayer.BusinessObjects.agent import Agent
import BusinessLayer.BusinessObjects.agent_factory as agent_factory
from DataLayer.DAO.dao_agent import DAOAgent
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
from utils.singleton import Singleton
from typing import List


class AgentService(metaclass=Singleton):
    @staticmethod
    def creer_agent(est_superviseur: bool, quotite: float, nom_utilisateur: str,
                    mot_de_passe: str, prenom: str, nom: str, id_superviseur: int = None) -> bool:
        data_agent = {'est_superviseur': est_superviseur, 'prenom': prenom, 'nom': nom, 'quotite': quotite,
                      'identifiant_superviseur': id_superviseur,
                      'identifiant_agent' : DAOAgent().recuperer_dernier_id_agent() + 1}
        nouvel_agent = agent_factory.AgentFactory.from_dict(data_agent)
        return DAOAgent().creer_agent(nouvel_agent, nom_utilisateur, mot_de_passe)

    @staticmethod
    def modifier_agent(agent_a_modifier: Agent) -> bool:
        return DAOAgent().modifier_agent(agent_a_modifier)

    @staticmethod
    def reinitialiser_identifiants(id_agent: int, nouveau_mot_de_passe_en_clair: str,
                                   nouveau_nom_utilisateur: str = None) -> bool:
        if nouveau_nom_utilisateur is None:
            nouveau_nom_utilisateur = DAOAgent().recuperer_nom_utilisateur(id_agent)
        res = DAOAgent().modifier_identifiants(id_agent, nouveau_nom_utilisateur,
                                               nouveau_mot_de_passe_en_clair)
        return res

    @staticmethod
    def changer_identifiants(id_agent: int, nom_utilisateur_actuel: str, mot_de_passe_actuel_en_clair: str,
                             nouveau_nom_utilisateur: str = None,
                             nouveau_mot_de_passe_en_clair: str = None) -> bool:
        validation_identifiants = DAOAgent().verifier_identifiants(id_agent, nom_utilisateur_actuel,
                                                                   mot_de_passe_actuel_en_clair)
        if validation_identifiants:
            if nouveau_nom_utilisateur is None:
                nouveau_nom_utilisateur = nom_utilisateur_actuel
            if nouveau_mot_de_passe_en_clair is None:
                nouveau_mot_de_passe_en_clair = mot_de_passe_actuel_en_clair
            return DAOAgent().modifier_identifiants(id_agent, nouveau_nom_utilisateur, nouveau_mot_de_passe_en_clair)
        else:
            return False

    @staticmethod
    def supprimer_agent(agent_a_supprimer: int) -> bool:
        pot_agent = DAOFicheAdresse().recuperer_pot(agent_a_supprimer)
        liste_id_pot = []
        for fiche in pot_agent:
            liste_id_pot.append(fiche.fiche_id)
        id_superviseur = DAOAgent().recuperer_id_superviseur(agent_a_supprimer)
        res_reaffect = DAOFicheAdresse().affecter_fiches_adresse(id_superviseur, liste_id_pot)
        res_suppr = False
        if res_reaffect:
            res_suppr = DAOAgent().supprimer_agent(agent_a_supprimer)
        return res_reaffect and res_suppr

    @staticmethod
    def recuperer_id_superviseur(id_agent: int) -> int:
        return DAOAgent().recuperer_id_superviseur(id_agent)

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
        return DAOAgent().promouvoir_agent(id_agent)

    @staticmethod
    def deleguer_agent(id_agent: List[int], id_delegue: int) -> bool:
        return DAOAgent().deleguer_agent(id_agent, id_delegue)

    @staticmethod
    def deleguer_equipe(id_superviseur: int, id_delegue: int) -> bool:
        return DAOAgent().deleguer_equipe(id_superviseur, id_delegue)

    @staticmethod
    def recuperer_agent(id_agent: int) -> Agent:
        return DAOAgent().recuperer_agent(id_agent)
