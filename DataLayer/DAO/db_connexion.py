import os

import DataLayer.DAO.interface_factory as factory
from utils.singleton import Singleton


class DBConnexion(metaclass=Singleton):
    
    def __init__(self):
        self.__interface = factory.InterfaceFactory.get_interface("Connexion")
        self.__connexion = self.__interface.ouvrir_connexion(os.environ["HOST"], os.environ["PORT"],
                                                             os.environ["DATABASE"],
                                                             os.environ["USER"], os.environ["PASSWORD"])
        if self.__connexion is None:
            raise ConnectionError

    @property
    def connexion(self):
        """
        return the opened connection.

        :return: the opened connection.
        """
        return self.__connexion

    def __del__(self):
        self.__interface.fermer_connexion(self.__connexion)
