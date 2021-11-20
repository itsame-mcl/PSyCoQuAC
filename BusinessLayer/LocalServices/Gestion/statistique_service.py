from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
from utils.singleton import Singleton


class StatistiqueService(metaclass=Singleton):

    @staticmethod
    def fiches_par_agent():
        res = DAOFicheAdresse().obtenir_statistiques(par_pot=True)
        return res

    @staticmethod
    def fiches_par_lot():
        res = DAOFicheAdresse().obtenir_statistiques(par_lot=True)
        return res

    @staticmethod
    def fiches_par_code_res():
        res = DAOFicheAdresse().obtenir_statistiques(par_code_resultat=True)
        return res
