from BusinessLayer.BusinessObjects.agent import Agent


class Superviseur(Agent):
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
