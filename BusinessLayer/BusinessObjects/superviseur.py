from BusinessLayer.BusinessObjects.agent import Agent


class Superviseur(Agent):
    def __init__(self, prenom: str, nom: str, quotite: float, agent_id: int = None):
        """

        :param prenom:
        :param nom:
        :param quotite:
        :param agent_id:
        """
        super().__init__(prenom, nom, quotite, agent_id)

    def as_dict(self) -> dict:
        """

        :return:
        """
        data = super().as_dict()
        data["identifiant_superviseur"] = self._agent_id
        data["est_superviseur"] = True
        return data
