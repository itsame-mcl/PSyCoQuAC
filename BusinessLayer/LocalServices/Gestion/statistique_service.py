from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
from utils.singleton import Singleton


class StatistiqueService(metaclass=Singleton):

    @staticmethod
    def fiches_par_agent():
        """

        :return:
        """
        res = DAOFicheAdresse().obtenir_statistiques(par_pot=True)
        return res

    @staticmethod
    def fiches_par_lot():
        """

        :return:
        """
        res = DAOFicheAdresse().obtenir_statistiques(par_lot=True)
        return res

    @staticmethod
    def lots_a_traiter_api(id_superviseur: int):
        """

        :param id_superviseur:
        :return:
        """
        lots = list()
        res = DAOFicheAdresse().obtenir_statistiques(par_lot=True, filtre_pot=-id_superviseur,
                                                     filtre_code_resultat="TA")
        for ligne in res:
            lots.append(ligne[0])
        return lots

    @staticmethod
    def lots_a_affecter(id_superviseur: int):
        """

        :param id_superviseur:
        :return:
        """
        lots = list()
        res = DAOFicheAdresse().obtenir_statistiques(par_lot=True, filtre_pot=-id_superviseur)
        for ligne in res:
            lots.append(ligne[0])
        rem = DAOFicheAdresse().obtenir_statistiques(par_lot=True, filtre_pot=-id_superviseur,
                                                     filtre_code_resultat="TA")
        for ligne in rem:
            lots.remove(ligne[0])
        return lots

    @staticmethod
    def fiches_par_code_res():
        """

        :return:
        """
        res = DAOFicheAdresse().obtenir_statistiques(par_code_resultat=True)
        return res
