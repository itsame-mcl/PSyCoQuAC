from abc import ABC, abstractmethod


class Agent(ABC):
    def __init__(self, prenom: str, nom: str, quotite: float, agent_id: int = None):
        self._agent_id = agent_id
        self._prenom = prenom
        self._nom = nom
        self._quotite = quotite

    @property
    def agent_id(self) -> int:
        return self._agent_id

    @property
    def prenom(self) -> str:
        return self._prenom

    @prenom.setter
    def prenom(self, value: str):
        self._prenom = value

    @property
    def nom(self) -> str:
        return self._nom

    @nom.setter
    def nom(self, value: str):
        self._nom = value

    @property
    def quotite(self) -> float:
        return self._quotite

    @quotite.setter
    def quotite(self, value):
        self._quotite = value

    @abstractmethod
    def as_dict(self) -> dict:
        data = dict()
        data["identifiant_agent"] = self._agent_id
        data["quotite"] = self._quotite
        data["prenom"] = self._prenom
        data["nom"] = self._nom
        return data
