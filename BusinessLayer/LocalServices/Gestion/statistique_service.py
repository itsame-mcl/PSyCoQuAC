from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
from utils.singleton import Singleton


class StatistiqueService(metaclass=Singleton):

    @staticmethod
    def fiches_par_agent():
        """

        :return:
        renvoie le nombre de fiches adresse dans le pot de chaque agent
        """
        res = DAOFicheAdresse().obtenir_statistiques(par_pot=True)
        return res

    @staticmethod
    def fiches_par_lot():
        """

        :return:
        renvoie le nombre de fiches adresse dans chaque lot qui a été importé
        """
        res = DAOFicheAdresse().obtenir_statistiques(par_lot=True)
        return res

    @staticmethod
    def fiches_par_code_res():
        """

        :return:
        renvoie le nombre de fiches adresse par code résultat
        """
        res = DAOFicheAdresse().obtenir_statistiques(par_code_resultat=True)
        return res
