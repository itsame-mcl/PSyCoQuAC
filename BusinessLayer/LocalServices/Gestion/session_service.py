from DataLayer.DAO.dao_agent import DAOAgent
from ViewLayer.CLI.session import Session
from utils.singleton import Singleton


class SessionService(metaclass=Singleton):
    @staticmethod
    def ouvrir_session(nom_utilisateur, mot_de_passe):
        """
        Cette méthode permet à un utilisateur de se connecter à l'application PSyCoQuAC,
        en renseignant son nom d'utilisateur et son mot de passe.

        :param nom_utilisateur:
        le nom d'utilisateur de l'agent cherchant à ouvrir sa session
        :param mot_de_passe:
        le mot de passe de l'agent cherchant à ouvrir sa session
        :return:
        renvoie un Business Object Agent dont le nom d'utilisateur et le mot de passe ont été passés en paramètres de la méthode
        """
        try:
            agent = DAOAgent().connexion_agent(nom_utilisateur, mot_de_passe)
        except ConnectionRefusedError:
            agent = None
        return agent

    def fermer_session(self):
        """
        cette méthode permet de fermer la session utilisateur actuellement ouverte.
        """
        Session.clear()
