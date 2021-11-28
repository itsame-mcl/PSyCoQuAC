from abc import ABC, abstractmethod
import attr


@attr.s
class Agent(ABC):
    """
        :param prenom:
        le prénom de l'agent
        :param nom:
        le nom de l'agent
        :param quotite:
        la quotité de travail de l'agent
        :param agent_id:
        l'identifiant, dans la base de données Agents, de l'agent
    """
    prenom: str = attr.ib(converter=str, on_setattr=attr.setters.convert)
    nom: str = attr.ib(converter=str, on_setattr=attr.setters.convert)
    quotite: float = attr.ib(converter=float, on_setattr=attr.setters.convert)
    agent_id: int = attr.ib(default=None, converter=attr.converters.optional(int), on_setattr=attr.setters.frozen)

    @abstractmethod
    def as_dict(self) -> dict:
        """
        Cette méthode transforme l'agent en dictionnaire, dont les valeurs sont les paramètres de l'agent.

        :return:
        renvoie un dictionnaire contenant les informations de l'agent
        """
        data = dict()
        data["identifiant_agent"] = self.agent_id
        data["quotite"] = self.quotite
        data["prenom"] = self.prenom
        data["nom"] = self.nom
        return data
