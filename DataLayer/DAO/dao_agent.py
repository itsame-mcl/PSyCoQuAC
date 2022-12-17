from typing import List
import BusinessLayer.BusinessObjects.agent_factory as agent_factory
import DataLayer.DAO.interface_factory as interface_factory
from BusinessLayer.BusinessObjects.agent import Agent
from BusinessLayer.BusinessObjects.gestionnaire import Gestionnaire
from BusinessLayer.BusinessObjects.superviseur import Superviseur
from utils.singleton import Singleton
from hashlib import sha512


class DAOAgent(metaclass=Singleton):
    def __init__(self):
        self.__interface = interface_factory.InterfaceFactory.get_interface("Agent")

    @staticmethod
    def __saler_hasher_mdp(nom_utilisateur: str, mot_de_passe_en_clair: str) -> str:
        """
        Cette méthode permet de saler/hacher le mot de passe et le nom d'utilisateur pris en arguments,
        selon l'algorithme sha512.

        :param nom_utilisateur:
        le nom d'utilisateur de l'agent
        :param mot_de_passe_en_clair:
        le mot de passe de l'agent, non salé/haché
        :return:
        renvoie le mot de passe de la base de données Agents, résultant du salage/hachage des paramètres pris en arguments
        """
        pwd = sha512()
        pwd.update(nom_utilisateur.encode("utf-8"))
        pwd.update(mot_de_passe_en_clair.encode("utf-8"))
        return pwd.hexdigest()

    def recuperer_agent(self, id_agent: int) -> Agent:
        """
        Cette méthode permet de récupérer le Business Object Agent
        correspondant à l'identifiant de la base de données Agents que l'on renseigne.

        :param id_agent:
        l'identifiant, dans la base de données Agents, de l'agent que l'on souhaite récupérer
        :return:
        renvoie le Business Object Agent dont l'identifiant a été passé en paramètre de la méthode
        """
        data = self.__interface.recuperer_agent(id_agent)
        return agent_factory.AgentFactory.from_dict(data)

    def recuperer_liste_superviseurs(self) -> List[Superviseur]:
        """
        Cette méthode permet de récupérer la liste des superviseurs enregistrés dans l'application PSyCoQuAC.

        :return:
        renvoie la liste des superviseurs présents dans la base de données Agents de l'application PsyCoQuAC
        """
        data = self.__interface.recuperer_liste_agents(0)
        liste = []
        for row in data:
            if row['est_superviseur']:
                liste.append(agent_factory.AgentFactory.from_dict(row))
        return liste

    def recuperer_equipe(self, id_superviseur: int) -> List[Agent]:
        """
        Cette méthode permet de récupérer la liste des agents qui compose l'équipe du superviseur
        dont on renseigne l'identifiant de la base de données Agents.

        :param id_superviseur:
        l'identifiant, dans la base de données Agents, du superviseur dont on cherche à récupérer l'équipe
        :return:
        renvoie la liste des agents composant l'équipe du superviseur
        """
        data = self.__interface.recuperer_liste_agents(id_superviseur)
        equipe = []
        for row in data:
            equipe.append(agent_factory.AgentFactory.from_dict(row))
        return equipe

    def recuperer_liste_delegues(self, id_superviseur: int) -> List[Gestionnaire]:
        """
        Cette méthode permet de récupérer la liste des agents de l'équipe du superviseur dont on renseigne l'identifiant de la base de données Agents,
        qui ont été délégués depuis une autre équipe.

        :param id_superviseur:
        l'identifiant, dans la base de données Agents, du superviseur de l'équipe dans laquelle on cherche les agents délégués
        :return:
        renvoie la liste des agents délégués présents dans l'équipe
        """
        data = self.__interface.recuperer_liste_agents(id_superviseur, True)
        equipe = []
        for row in data:
            if not row['est_superviseur']:
                equipe.append(agent_factory.AgentFactory.from_dict(row))
        return equipe

    def deleguer_agent(self, id_agent: int, id_delegue: int) -> bool:
        """
        Cette méthode permet de déléguer l'agent dont on renseigne l'identifiant de la base de données Agents,
        dans l'équipe du superviseur dont on renseigne l'identifiant de la base de données Agents,
        de manière temporaire.

        :param id_agent:
        l'identifiant, dans la base de données Agents, de l'agent que l'on souhaite déléguer dans une autre équipe
        :param id_delegue:
        l'identifiant, dans la base de données Agents, du superviseur de l'équipe dans laquelle on souhaite déléguer l'équipe
        :return:
        renvoie un booléen valant True si l'agent a été correctement délégué dans sa nouvelle équipe
        """
        return self.__interface.deleguer_agent(id_agent, id_delegue)

    def retroceder_agent(self, id_agent: int) -> bool:
        """
        Cette méthode permet de placer l'agent, dont on renseigne l'identifiant de la base de données Agents,
        dans son équipe d'origine.

        :param id_agent:
        l'identifiant, dans la base de données Agents, de l'agent que l'on souhaite rétrocéder à son superviseur initial
        :return:
        renvoie un booléen valant True si l'agent a été correctement rétrocédé à son superviseur initial
        """
        return self.__interface.retroceder_agent(id_agent)

    def transferer_agent(self, id_agent: int, id_nouveau_superviseur: int) -> bool:
        """
        Cette méthode permet de transférer l'agent dont on renseigne l'identifiant de la base de données Agents,
        dans l'équipe du superviseur dont on renseigne l'identifiant de la base de données Agents,
        de manière définitive.

        :param id_agent:
        l'identifiant, dans la base de données Agents, de l'agent que l'on souhaite transférer dans une autre équipe
        :param id_nouveau_superviseur:
        l'identifiant, dans la base de données Agents, du superviseur de l'équipe dans laquelle on souhaite transférer l'équipe 
        :return:
        renvoie un booléen valant True si l'agent a été correctement transféré dans sa nouvelle équipe
        """
        return self.__interface.transferer_agent(id_agent, id_nouveau_superviseur)

    def creer_agent(self, infos_agent: Agent, nom_utilisateur: str, mot_de_passe: str) -> bool:
        """
        Cette méthode permet de créer un agent dans la base de données Agents.

        :param infos_agent:
        les informations de l'agent que l'on souhaite créer
        :param nom_utilisateur:
        le nom d'utilisateur de l'agent que l'on souhaite créer
        :param mot_de_passe_en_clair:
        le mot de passe, non salé/haché, de l'agent que l'on souhaite créer
        :return:
        renvoie un booléen valant True si l'agent a été correctement créé
        """
        data = infos_agent.as_dict()
        if data['est_superviseur'] and data['identifiant_superviseur'] is None:
            data['identifiant_superviseur'] = self.__interface.recuperer_dernier_id_agent() + 1
        data["nom_utilisateur"] = nom_utilisateur
        data["mot_de_passe"] = self.__saler_hasher_mdp(nom_utilisateur, mot_de_passe)
        return self.__interface.creer_agent(data)

    def modifier_agent(self, agent_a_modifier: Agent) -> bool:
        """
        Cette méthode permet de modifier les informations d'un agent dans la base de données Agents.

        :param agent_a_modifier:
        l'agent dont on souhaite modifier les informations
        :return:
        renvoie un Agent, dont les informations dans la base de données Agents ont été modifiées
        """
        return self.__interface.modifier_agent(agent_a_modifier.as_dict())

    def supprimer_agent(self, id_agent: int) -> bool:
        """
        Cette méthode permet de supprimer un agent de la base de données Agents, et donc de l'application PSyCoQuAC.

        :param id_agent:
        l'identifiant, dans la base de données Agents, de l'agent à supprimer
        :return:
        renvoie un booléen valant True si l'agent a été correctement supprimé
        """
        return self.__interface.supprimer_agent(id_agent)

    def promouvoir_agent(self, agent_a_promouvoir: int) -> bool:
        """
        Cette méthode permet de promouvoir l'agent dont on renseigne l'identifiant de la base de données Agents,
        c'est-à-dire de transformer un gestionnaire en superviseur. 

        :param agent_a_promouvoir:
        l'identifiant, dans la base de données Agents, de l'agent que l'on souhaite promouvoir
        :return:
        renvoie un booléen valant True si l'agent a été correctement promu
        """
        return self.__interface.promouvoir_agent(agent_a_promouvoir)

    def connexion_agent(self, nom_utilisateur: str, mot_de_passe: str) -> Agent:
        """
        Cette méthode permet à un agent de se connecter, en rentrant son nom d'utilisateur et son mot de passe,
        qui vont être salées/hachés afin que le résultat soit comparé aux mots de passe enregistrés dans la base de données Agents,
        afin de renvoyer (s'il existe) l'agent correspondant. 

        :param nom_utilisateur:
        le nom d'utilisateur de l'agent cherchant à se connecter
        :param mot_de_passe_en_clair:
        le mot de passe, non salé/haché, de l'agent cherchant à se connecter
        :return:
        renvoie le Business Object Agent correspondant à l'agent connecté
        """
        mot_de_passe_sale_hashe = self.__saler_hasher_mdp(nom_utilisateur, mot_de_passe)
        data = self.__interface.connexion_agent(nom_utilisateur, mot_de_passe_sale_hashe)
        if data is not None:
            agent = agent_factory.AgentFactory.from_dict(data)
            return agent
        raise ConnectionRefusedError

    def modifier_identifiants(self, id_agent: int, nom_utilisateur: str, mot_de_passe_en_clair: str) -> bool:
        """
        Cette méthode permet de modifier les identifiants (nom d'utilisateur et mot de passe)
        de l'agent dont on renseigne l'identifiant de la base de données Agents.

        :param id_agent:
        l'identifiant, dans la base de données Agents, de l'agent dont on souhaite modifier les identifiants
        :param nom_utilisateur:
        le nom d'utilisateur de l'agent dont on souhaite modifier les identifiants
        :param mot_de_passe_en_clair:
        le mot de passe, non salé/haché, de l'agent dont on souhaite modifier les identifiants
        :return:
        renvoie un booléen valant True si les identifiants de l'agent ont été correctement modifiés
        """
        mdp_sale_hashe = self.__saler_hasher_mdp(nom_utilisateur, mot_de_passe_en_clair)
        res = self.__interface.modifier_identifiants(id_agent, nom_utilisateur, mdp_sale_hashe)
        return res

    def verifier_identifiants(self, id_agent: int, nom_utilisateur: str, mot_de_passe_en_clair: str) -> bool:
        """
        Cette méthode permet de vérifier les identifiants de l'agent dont on renseigne l'identifiant de la base de données Agents,
        en comparant le salage/hachage du nom d'utilisateur et du mot de passe renseignés en arguments,
        avec le mot de passe salé/haché enregistré dans la base de données Agents correspondant à l'identifiant de l'agent.

        :param id_agent:
        l'identifiant, dans la base de données Agents, de l'agent dont on souhaite vérifier les identifiants
        :param nom_utilisateur:
        le nom d'utilisateur de l'agent dont on souhaite vérifier les identifiants
        :param mot_de_passe_en_clair:
        le mot de passe, non salé/haché, de l'agent dont on souhaite vérifier les identifiants
        :return:
        renvoie un booléen valant True si les identifiants de l'agent ont été correctement vérifiés
        """
        mdp_sale_hashe = self.__saler_hasher_mdp(nom_utilisateur, mot_de_passe_en_clair)
        res = self.__interface.verifier_identifiants(id_agent, nom_utilisateur, mdp_sale_hashe)
        return res

    def recuperer_quotite(self, id_agent: int) -> float:
        """
        Cette méthode permet de récupérer le nom d'utilisateur, dans la base de données Agents,
        de l'agent dont on renseigne l'identifiant de la base de données Agents.

        :param id_agent:
        l'identifiant, dans la base de données Agents, de l'agent dont on cherche à récupérer le nom d'utilisateur
        :return:
        la quotité de travail de l'agent dont on a renseigné l'identifiant de la base de données Agents
        """
        return self.__interface.recuperer_quotite(id_agent)

    def recuperer_nom_utilisateur(self, id_agent: int) -> str:
        """
        Cette méthode permet de récupérer le nom d'utilisateur, dans la base de données Agents,
        de l'agent dont on renseigne l'identifiant de la base de données Agents.

        :param id_agent:
        l'identifiant, dans la base de données Agents, de l'agent dont on cherche à récupérer le nom d'utilisateur
        :return:
        le nom d'utilisateur de l'agent dont on a renseigné l'identifiant de la base de données Agents
        """
        return self.__interface.recuperer_nom_utilisateur(id_agent)

    def recuperer_dernier_id_agent(self) -> int:
        """
        Cette méthode permet de récupérer le dernier identifiant d'agent de la base de données Agents,
        c'est-à-dire l'identifiant attribué en dernier à un agent dans la base de données Agents.

        :return:
        renvoie le dernier identifiant d'agent de la base de données Agents
        """
        return self.__interface.recuperer_dernier_id_agent()

    def recuperer_id_superviseur(self, id_agent: int) -> int:
        """
        Cette méthode permet de récupérer l'identifiant, dans la base de données Agents, du superviseur 
        de l'agent dont on renseigne l'identifiant de la base de données Agents.

        :param id_agent:
        l'identifiant, dans la base de données Agents, de l'agent dont on cherche à récupérer l'identifiant du superviseur
        :return:
        renvoie l'identifiant, dans la base de données Agents, du superviseur de l'équipe de l'agent
        """
        return self.__interface.recuperer_id_superviseur(id_agent)
