from BusinessLayer.BusinessObjects.agent import Agent


class Superviseur(Agent):
    def __init__(self, prenom: str, nom: str, quotite: float, agent_id: int = None):
        """

        :param prenom:
        le prénom du superviseur
        :param nom:
        le nom du superviseur
        :param quotite:
        la quotité de travail du superviseur
        :param agent_id:
        l'identifiant, dans la base de données Agents, du superviseur
        """
        super().__init__(prenom, nom, quotite, agent_id)

    def as_dict(self) -> dict:
        """

        :return:
        renvoie un dictionnaire contenant les informations du superviseur
        """
        data = super().as_dict()
        data["identifiant_superviseur"] = self._agent_id
        data["est_superviseur"] = True
        return data
