from BusinessLayer.BusinessObjects.gestionnaire import Gestionnaire
from BusinessLayer.BusinessObjects.superviseur import Superviseur


class AgentFactory:
    @staticmethod
    def from_dict(data: dict):
        """

        :param data:
        un dictionnaire de données correspondant aux informations sur l'agent que l'on va créer
        :return:
        renvoie un objet de type agent
        """
        if data["est_superviseur"]:
            agent = Superviseur(data["prenom"], data["nom"], data["quotite"], data["identifiant_agent"])
        else:
            agent = Gestionnaire(data["prenom"], data["nom"], data["quotite"],
                                 data["identifiant_superviseur"], data["identifiant_agent"])
        return agent
