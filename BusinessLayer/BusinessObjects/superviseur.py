from BusinessLayer.BusinessObjects.agent import Agent


class Superviseur(Agent):
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
    def as_dict(self) -> dict:
        """
        Cette méthode transforme le superviseur en dictionnaire,
        dont les valeurs sont les paramètres du superviseur.

        :return:
        renvoie un dictionnaire contenant les informations du superviseur
        """
        data = super().as_dict()
        data["identifiant_superviseur"] = self.agent_id
        data["est_superviseur"] = True
        return data
