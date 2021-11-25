from BusinessLayer.BusinessObjects.agent import Agent
import BusinessLayer.BusinessObjects.agent_factory as agent_factory
from BusinessLayer.BusinessObjects.gestionnaire import Gestionnaire
from BusinessLayer.BusinessObjects.superviseur import Superviseur
from DataLayer.DAO.dao_agent import DAOAgent
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
from utils.singleton import Singleton
from typing import List


class AgentService(metaclass=Singleton):
    @staticmethod
    def creer_agent(est_superviseur: bool, quotite: float, nom_utilisateur: str,
                    mot_de_passe: str, prenom: str, nom: str, id_superviseur: int = None) -> bool:
        """
        Cette méthode permet de créer un agent dans la base de données Agents,
        dont les paramètres sont les arguments de cette fonction.

        :param est_superviseur:
        un booléen valant True si l'agent créé est un superviseur, et False si c'est un gestionnaire
        :param quotite:
        la quotité de travail de l'agent créé
        :param nom_utilisateur:
        le nom d'utilisateur de l'agent créé
        :param mot_de_passe:
        le mot de passe de l'agent créé
        :param prenom:
        le prénom de l'agent créé
        :param nom:
        le nom de l'agent créé
        :param id_superviseur:
        l'identifiant, dans la base de données Agents, du superviseur de l'équipe de l'agent créé, si ce dernier est un gestionnaire 
        :return:
        renvoie un Agent, dont les informations sont les paramètres de la fonction creer_agent
        """
        data_agent = {'est_superviseur': est_superviseur, 'prenom': prenom, 'nom': nom, 'quotite': quotite,
                      'identifiant_superviseur': id_superviseur,
                      'identifiant_agent': DAOAgent().recuperer_dernier_id_agent() + 1}
        nouvel_agent = agent_factory.AgentFactory.from_dict(data_agent)
        return DAOAgent().creer_agent(nouvel_agent, nom_utilisateur, mot_de_passe)

    @staticmethod
    def modifier_agent(agent_a_modifier: Agent) -> bool:
        """
        Cette méthode permet de modifier les informations d'un agent dans la base de données Agents.

        :param agent_a_modifier:
        l'agent dont on souhaite modifier les informations
        :return:
        renvoie un Agent, dont les informations dans la base de données Agents ont été modifiées
        """
        return DAOAgent().modifier_agent(agent_a_modifier)

    @staticmethod
    def reinitialiser_identifiants(id_agent: int, nouveau_mot_de_passe_en_clair: str,
                                   nouveau_nom_utilisateur: str = None) -> bool:
        """
        Cette méthode permet de réinitialiser les identifiants permettant à un agent de se connecter à l'application PSyCoQuAC.

        :param id_agent:
        le nouvel identifiant de l'agent dans la base de données Agents
        :param nouveau_mot_de_passe_en_clair:
        le nouveau mot de passe, non haché/salé avec le nom d'utilisateur, de l'agent
        :param nouveau_nom_utilisateur:
        le nouveau nom d'utilisateur de l'agent
        :return:
        renvoie un booléen valant True si les identifiants de l'agent ont été correctement réinitialisés
        """
        if nouveau_nom_utilisateur is None:
            nouveau_nom_utilisateur = DAOAgent().recuperer_nom_utilisateur(id_agent)
        res = DAOAgent().modifier_identifiants(id_agent, nouveau_nom_utilisateur,
                                               nouveau_mot_de_passe_en_clair)
        return res

    @staticmethod
    def changer_identifiants(id_agent: int, nom_utilisateur_actuel: str, mot_de_passe_actuel_en_clair: str,
                             nouveau_nom_utilisateur: str = None,
                             nouveau_mot_de_passe_en_clair: str = None) -> bool:
        """
        Cette méthode permet de changer les identifiants permettant à un agent de se connecter à l'application PSyCoQuAC. 

        :param id_agent:
        l'identifiant, dans la base de données Agents, de l'agent
        :param nom_utilisateur_actuel:
        le nom d'utilisateur actuel de l'agent
        :param mot_de_passe_actuel_en_clair:
        le mot de passe actuel de l'agent, non haché/salé avec le nom d'utilisateur
        :param nouveau_nom_utilisateur:
        le nouveau nom d'utilisateur de l'agent
        :param nouveau_mot_de_passe_en_clair:
        le nouveau mot de passe de l'agent, non haché/salé avec le nom d'utilisateur
        :return:
        renvoie un booléen valant True si les identifiants de l'agent ont été correctement changés
        """
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
        """
        Cette méthode permet de supprimer un agent de la base de données Agents, et donc de l'application PSyCoQuAC.
        En supprimant cet agent, les fiches adresse de son pot (si ce dernier n'est pas vide) sont redonnées à son superviseur.

        :param agent_a_supprimer:
        l'identifiant, dans la base de données Agents, de l'agent à supprimer
        :return:
        renvoie un couple de booléen, dont le premier vaut True si le pot de l'agent supprimé ont été correctement réaffectées,
        et dont le second vaut un booléen valant True si l'agent a été correctement supprimé
        """
        pot_agent = DAOFicheAdresse().recuperer_pot(agent_a_supprimer)
        liste_id_pot = []
        for fiche in pot_agent:
            liste_id_pot.append(fiche.fiche_id)
        id_superviseur = DAOAgent().recuperer_id_superviseur(agent_a_supprimer)
        if len(liste_id_pot) > 0:
            res_reaffect = DAOFicheAdresse().affecter_fiches_adresse(id_superviseur, liste_id_pot)
        else:
            res_reaffect = True
        res_suppr = False
        if res_reaffect:
            res_suppr = DAOAgent().supprimer_agent(agent_a_supprimer)
        return res_reaffect and res_suppr

    @staticmethod
    def recuperer_id_superviseur(id_agent: int) -> int:
        """
        Cette méthode permet de récupérer l'identifiant, dans la base de données Agents, du superviseur 
        de l'agent dont on renseigne l'identifiant de la base de données Agents.

        :param id_agent:
        l'identifiant, dans la base de données Agents, de l'agent dont on cherche à récupérer l'identifiant du superviseur
        :return:
        renvoie l'identifiant, dans la base de données Agents, du superviseur de l'équipe de l'agent
        """
        return DAOAgent().recuperer_id_superviseur(id_agent)

    @staticmethod
    def recuperer_equipe(id_superviseur: int) -> List[Agent]:
        """
        Cette méthode permet de récupérer la liste des agents qui compose l'équipe du superviseur
        dont on renseigne l'identifiant de la base de données Agents.

        :param id_superviseur:
        l'identifiant, dans la base de données Agents, du superviseur dont on cherche à récupérer l'équipe
        :return:
        renvoie la liste des agents composant l'équipe du superviseur
        """
        return DAOAgent().recuperer_equipe(id_superviseur)

    @staticmethod
    def recuperer_liste_delegues(id_superviseur: int) -> List[Gestionnaire]:
        """
        Cette méthode permet de récupérer la liste des agents de l'équipe du superviseur dont on renseigne l'identifiant de la base de données Agents,
        qui ont été délégués depuis une autre équipe.

        :param id_superviseur:
        l'identifiant, dans la base de données Agents, du superviseur de l'équipe dans laquelle on cherche les agents délégués
        :return:
        renvoie la liste des agents délégués présents dans l'équipe
        """
        return DAOAgent().recuperer_liste_delegues(id_superviseur)

    @staticmethod
    def recuperer_liste_superviseurs() -> List[Superviseur]:
        """
        Cette méthode permet de récupérer la liste des superviseurs enregistrés dans l'application PSyCoQuAC.

        :return:
        renvoie la liste des superviseurs enregistrés dans l'application
        """
        return DAOAgent().recuperer_liste_superviseurs()

    @staticmethod
    def promouvoir_agent(id_agent: int) -> bool:
        """
        Cette méthode permet de promouvoir l'agent dont on renseigne l'identifiant de la base de données Agents,
        c'est-à-dire de transformer un gestionnaire en superviseur. 

        :param id_agent:
        l'identifiant, dans la base de données Agents, de l'agent que l'on souhaite promouvoir
        :return:
        renvoie un booléen valant True si l'agent a été correctement promu
        """
        return DAOAgent().promouvoir_agent(id_agent)

    @staticmethod
    def deleguer_agent(id_agent: int, id_delegue: int) -> bool:
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
        return DAOAgent().deleguer_agent(id_agent, id_delegue)

    @staticmethod
    def transferer_agent(id_agent: int, id_nouveau_superviseur: int) -> bool:
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
        return DAOAgent().transferer_agent(id_agent, id_nouveau_superviseur)

    @staticmethod
    def retroceder_agent(id_agent: int) -> bool:
        """
        Cette méthode permet de placer l'agent, dont on renseigne l'identifiant de la base de données Agents,
        dans son équipe d'origine.

        :param id_agent:
        l'identifiant, dans la base de données Agents, de l'agent que l'on souhaite rétrocéder à son superviseur initial
        :return:
        renvoie un booléen valant True si l'agent a été correctement rétrocédé à son superviseur initial
        """
        return DAOAgent().retroceder_agent(id_agent)

    @staticmethod
    def recuperer_agent(id_agent: int) -> Agent:
        """
        Cette méthode permet de récupérer le Business Object Agent
        correspondant à l'identifiant de la base de données Agents que l'on renseigne.

        :param id_agent:
        l'identifiant, dans la base de données Agents, de l'agent que l'on souhaite récupérer
        :return:
        renvoie le Business Object Agent dont l'identifiant a été passé en paramètre de la méthode
        """
        return DAOAgent().recuperer_agent(id_agent)
