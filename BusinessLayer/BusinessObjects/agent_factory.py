from BusinessLayer.BusinessObjects.gestionnaire import Gestionnaire
from BusinessLayer.BusinessObjects.superviseur import Superviseur


class AgentFactory:
    @staticmethod
    def from_dict(data: dict):
        """

        :param data:
        :return:
        """
        if data["est_superviseur"]:
            agent = Superviseur(data["prenom"], data["nom"], data["quotite"], data["identifiant_agent"])
        else:
            agent = Gestionnaire(data["prenom"], data["nom"], data["quotite"],
                                 data["identifiant_superviseur"], data["identifiant_agent"])
        return agent
