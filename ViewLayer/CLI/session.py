from utils.singleton import Singleton
from BusinessLayer.BusinessObjects.agent import Agent
from BusinessLayer.BusinessObjects.superviseur import Superviseur


class Session(metaclass=Singleton):

    def __init__(self):
        """
        Définition des variables que l'on stocke en session
        Le syntaxe
        ref:type = valeur
        permet de donner le type des variables. Utile pour l'autocompletion.
        """
        self.__agent = None
        self.__droits = None

    @property
    def agent(self):
        return self.__agent

    @agent.setter
    def agent(self, value: Agent):
        self.__agent = value
        self.__droits = isinstance(self.__agent, Superviseur)

    @property
    def droits(self):
        return self.__droits
