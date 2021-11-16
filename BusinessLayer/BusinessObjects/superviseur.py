from BusinessLayer.BusinessObjects.agent import Agent


class Superviseur(Agent):
    def __init__(self, prenom: str, nom: str, quotite: float, agent_id: int = None):
        super().__init__(prenom, nom, quotite, agent_id)

    def as_dict(self) -> dict:
        data = super().as_dict()
        data["identifiant_superviseur"] = self._agent_id
        data["est_superviseur"] = True
        return data
