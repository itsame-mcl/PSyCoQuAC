from BusinessLayer.BusinessObjects.agent import Agent
import attr


@attr.s
class Gestionnaire(Agent):
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
    superviseur_id: int = attr.ib(kw_only=True, converter=int, on_setattr=attr.setters.convert)

    def as_dict(self) -> dict:
        """
        Cette méthode transforme le gestionnaire en dictionnaire,
        dont les valeurs sont les paramètres du gestionnaire.

        :return:
        renvoie un dictionnaire contenant les informations du gestionnaire
        """
        data = super().as_dict()
        data["identifiant_superviseur"] = self.superviseur_id
        data["est_superviseur"] = False
        return data
