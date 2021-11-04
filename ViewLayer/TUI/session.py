from utils.singleton import Singleton
from BusinessLayer.BusinessObjects.agent import Agent
from BusinessLayer.BusinessObjects.superviseur import Superviseur

class Session(metaclass=Singleton):

    def __init__(self, agent : Agent):
        """
        Définition des variables que l'on stocke en session
        Le syntaxe
        ref:type = valeur
        permet de donner le type des variables. Utile pour l'autocompletion.
        """
        self.agent_id = agent.agent_id
        self.droits = isinstance(agent, Superviseur)