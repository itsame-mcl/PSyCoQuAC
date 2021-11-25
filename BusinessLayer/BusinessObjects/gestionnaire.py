from BusinessLayer.BusinessObjects.agent import Agent


class Gestionnaire(Agent):
    def __init__(self, prenom: str, nom: str, quotite: float, superviseur_id: int, agent_id: int = None):
        """

        :param prenom:
        le prénom du gestionnaire
        :param nom:
        le nom du gestionnaire
        :param quotite:
        la quotité de travail du gestionnaire
        :param superviseur_id:
        l'identifiant, dans la base de données Agents, du superviseur de l'équipe du gestionnaire
        :param agent_id:
        l'identifiant, dans la base de données Agents, du gestionnaire
        """
        super().__init__(prenom, nom, quotite, agent_id)
        self._superviseur_id = superviseur_id

    @property
    def superviseur_id(self) -> int:
        return self._superviseur_id

    @superviseur_id.setter
    def superviseur_id(self, value: int):
        self._superviseur_id = value

    def as_dict(self) -> dict:
        """
        Cette méthode transforme le gestionnaire en dictionnaire,
        dont les valeurs sont les paramètres du gestionnaire.

        :return:
        renvoie un dictionnaire contenant les informations du gestionnaire
        """
        data = super().as_dict()
        data["identifiant_superviseur"] = self._superviseur_id
        data["est_superviseur"] = False
        return data
